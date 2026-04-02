"""
Management command to ingest Handbook.pdf into the Knowledge Base using pure text extraction.

Since the PDF has been updated to be text-based, this bypasses the Gemini Vision API
image uploading and uses PyMuPDF (fitz) to extract text directly. The raw extracted text
is then sent to Gemini to fix any copy-paste or formatting errors, and chunked.
"""
import os
import re
import time
import logging

from django.conf import settings
from django.core.management.base import BaseCommand

import fitz  # PyMuPDF
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

from chatbot.models import FAQ

logger = logging.getLogger(__name__)

TEXT_CLEANUP_PROMPT = """You are an editor for the St. Paul University Surigao (SPUS) Student Handbook.
The following text was extracted from a PDF but contains formatting, layout, or copy-paste errors.

INSTRUCTIONS:
1. Clean up and format the text properly. Fix any broken sentences, bad spacing, or typos caused by extraction.
2. Structure it cleanly, maintaining any headers (put them on their own line in UPPERCASE), paragraphs, and lists.
3. Completely remove any meaningless strings, page numbers, footnotes, or garbage text.
4. Return ONLY the cleaned text, without any conversational filler or commentary.
5. If the extracted text is completely empty or just garbage, reply with [BLANK].

Raw Extracted Text:
"""

class Command(BaseCommand):
    help = 'Ingest text-based Handbook.pdf into the Knowledge Base using Gemini and PyMuPDF'

    def add_arguments(self, parser):
        parser.add_argument(
            '--pdf-path',
            type=str,
            default='Handbook.pdf',
            help='Path to the Handbook PDF file (default: Handbook.pdf)'
        )
        parser.add_argument(
            '--start-page',
            type=int,
            default=1,
            help='Start processing from this page number (1-indexed, default: 1)'
        )
        parser.add_argument(
            '--end-page',
            type=int,
            default=None,
            help='Stop processing at this page number (inclusive)'
        )
        parser.add_argument(
            '--chunk-size',
            type=int,
            default=900,
            help='Target chunk size in characters (default: 900)'
        )
        parser.add_argument(
            '--delay',
            type=float,
            default=4.5,
            help='Delay in seconds between API calls to respect rate limit (default: 4.5)'
        )
        parser.add_argument(
            '--clear-first',
            action='store_true',
            help='Clear existing Handbook FAQs before ingesting'
        )

    def handle(self, *args, **options):
        pdf_path = options['pdf_path']
        start_page = options['start_page']
        end_page = options['end_page']
        chunk_size = options['chunk_size']
        delay = options['delay']
        clear_first = options['clear_first']

        if not os.path.exists(pdf_path):
            self.stderr.write(self.style.ERROR(f"PDF file not found: {pdf_path}"))
            return
            
        if clear_first:
            self.stdout.write(self.style.WARNING("Clearing existing Student Handbook FAQs..."))
            deleted, _ = FAQ.objects.filter(category="Student Handbook").delete()
            self.stdout.write(f"Deleted {deleted} old FAQ entries.")

        api_key = settings.GEMINI_API_KEY
        if not api_key:
            self.stderr.write(self.style.ERROR("GEMINI_API_KEY is not set in .env."))
            return

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        self.stdout.write(f"Opened '{pdf_path}' — {total_pages} pages detected")

        if end_page is None:
            end_page = total_pages

        start_page = max(1, start_page)
        end_page = min(total_pages, end_page)

        self.stdout.write(f"Processing pages {start_page} to {end_page}...")

        all_chunks = []
        failed_pages = []

        for page_num in range(start_page - 1, end_page):
            page_display = page_num + 1
            self.stdout.write(f"\n{'='*60}")
            self.stdout.write(f"  Processing page {page_display}/{end_page}...")

            try:
                page = doc[page_num]
                raw_text = page.get_text()
                
                if not raw_text or len(raw_text.strip()) < 10:
                    self.stdout.write(self.style.WARNING(f"  Page {page_display}: No meaningful text found — skipping"))
                    continue

                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        self.stdout.write(f"  Cleaning {len(raw_text)} extracted chars via Gemini... (Attempt {attempt+1})")
                        response = model.generate_content(TEXT_CLEANUP_PROMPT + raw_text)
                        cleaned_text = response.text.strip()
                        break
                    except ResourceExhausted as e:
                        if attempt < max_retries - 1:
                            self.stdout.write(self.style.WARNING("  Rate limited (ResourceExhausted). Sleeping 65s before retry..."))
                            time.sleep(65)
                        else:
                            self.stderr.write(self.style.ERROR(f"  Failed after {max_retries} attempts due to rate limits."))
                            raise e

                if not cleaned_text or cleaned_text == "[BLANK]" or "[BLANK]" in cleaned_text:
                    self.stdout.write(self.style.WARNING(f"  Page {page_display}: Model returned BLANK — skipped"))
                    time.sleep(delay)
                    continue

                chunks = self._chunk_text(cleaned_text, chunk_size, page_display)
                self.stdout.write(f"  Page {page_display}: Extracted {len(cleaned_text)} cleaned chars -> {len(chunks)} chunk(s)")

                for chunk_info in chunks:
                    all_chunks.append(chunk_info)

                    obj, created = FAQ.objects.get_or_create(
                        category="Student Handbook",
                        question=chunk_info['question'],
                        defaults={'answer': chunk_info['answer']}
                    )
                    status = "CREATED" if created else "EXISTS"
                    self.stdout.write(f"    [{status}] {chunk_info['question']}")

                time.sleep(delay)

            except Exception as e:
                failed_pages.append(page_display)
                self.stderr.write(self.style.ERROR(f"  Page {page_display}: FAILED — {str(e)}"))
                time.sleep(delay)
                continue

        doc.close()

        if all_chunks:
            self.stdout.write(f"\n{'='*60}")
            self.stdout.write("Generating vector embeddings for new entries...")
            try:
                from chatbot.rag import RAGSearcher
                rag = RAGSearcher()
                rag.ensure_embeddings()
                self.stdout.write(self.style.SUCCESS("Embeddings generated successfully!"))
            except Exception as e:
                self.stderr.write(self.style.WARNING(f"Could not generate embeddings immediately: {e}"))

        self.stdout.write(f"\n{'='*60}")
        self.stdout.write(f"INGESTION COMPLETE")
        self.stdout.write(f"  Pages processed: {end_page - start_page + 1}")
        self.stdout.write(f"  Chunks created:  {len(all_chunks)}")
        self.stdout.write(f"  Failed pages:    {len(failed_pages)}")
        
        total_handbook = FAQ.objects.filter(category="Student Handbook").count()
        self.stdout.write(f"  Total handbook FAQs in DB: {total_handbook}")

    def _chunk_text(self, text, target_size, page_num):
        chunks = []
        lines = text.split('\n')
        page_title = None
        for line in lines:
            stripped = line.strip()
            if stripped and len(stripped) > 3:
                page_title = stripped[:80]
                break

        if not page_title:
            page_title = f"Page {page_num}"

        paragraphs = re.split(r'\n\s*\n', text)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]

        current_chunk = ""
        chunk_idx = 1

        for para in paragraphs:
            if current_chunk and len(current_chunk) + len(para) + 2 > target_size:
                chunks.append({
                    'question': f"Handbook: {page_title} (Page {page_num}, Part {chunk_idx})",
                    'answer': current_chunk.strip()
                })
                chunk_idx += 1
                current_chunk = para
            else:
                if current_chunk:
                    current_chunk += "\n\n" + para
                else:
                    current_chunk = para

        if current_chunk.strip():
            question = f"Handbook: {page_title} (Page {page_num})" if chunk_idx == 1 else f"Handbook: {page_title} (Page {page_num}, Part {chunk_idx})"
            chunks.append({
                'question': question,
                'answer': current_chunk.strip()
            })

        return chunks
