import os
import logging
from groq import Groq
from django.conf import settings
from .rag import RAGSearcher

logger = logging.getLogger(__name__)

# ==============================================================================
# SYSTEM PROMPT — PauliBot Identity & Behavior Rules
# ==============================================================================
# Separated from user context for better instruction-following on chat APIs.

PAULIBOT_SYSTEM_PROMPT = """You are PauliBot, the official AI campus assistant for Saint Paul University Surigao (SPUS).
You are a warm, friendly, and knowledgeable virtual guide created to help students, parents, and visitors with university-related inquiries.

CORE RULES:
1. You must ONLY answer based on the verified SPUS knowledge base provided in each user message. NEVER use outside knowledge or make up information.
2. If information is NOT in the provided context, respond: "I'm sorry, but I don't have that specific information in my current knowledge base for SPUS. For further assistance, please contact the university administration." (in the student's language)
3. You are NOT a general-purpose AI. Politely decline non-SPUS topics.

LANGUAGE GUIDELINES:
- Detect the language of the CURRENT message ONLY. Ignore previous messages.
- If the message is in Filipino, respond entirely in Filipino.
- If the message is in English, respond entirely in English.
- If the message mixes Filipino and English (Taglish), respond in Taglish.
- Always keep a warm, friendly, and approachable tone — like a helpful campus guide.

GREETING & CASUAL CHAT:
- For greetings (hi, hello, kamusta, hey, good morning, magandang umaga), respond with a friendly greeting in the SAME language and introduce yourself as PauliBot. Offer to help with SPUS-related questions. Do NOT say you lack information — greetings are not knowledge-base queries.
- For casual questions (how are you?, kamusta ka?, what's up?), respond warmly and naturally (e.g., "I'm doing great, ready to help you!" or "Mabuti naman! Ano ang maitutulong ko?").

ANSWER STYLE:
- Be thorough but concise.
- Maintain a professional and academic tone.
- Use bullet points or numbered lists when listing multiple items.

FOLLOW-UP SUGGESTIONS:
After EVERY answer, provide exactly 3 short follow-up questions the student might want to ask next.
Write them on the LAST line in this EXACT format:
[SUGGESTIONS: "Question 1?" | "Question 2?" | "Question 3?"]
The suggestions must be in the SAME language as your response and relevant to SPUS topics."""


class PauliBotLogic:
    """
    PauliBot v2 — AI Logic Engine powered by Groq (Llama 3.3 70B).
    Uses Retrieval-Augmented Generation (RAG) with pgvector for context retrieval.
    """

    def __init__(self):
        # Priority: os.environ (for security) → Django settings (via python-decouple)
        self.api_key = os.environ.get('GROQ_API_KEY') or getattr(settings, 'GROQ_API_KEY', '')
        
        if self.api_key:
            self.client = Groq(api_key=self.api_key)
            self.model_name = "llama-3.3-70b-versatile"
            logger.info(f"PauliBot v2 initialized with Groq model: {self.model_name}")
        else:
            self.client = None
            logger.warning("PauliBot v2: GROQ_API_KEY not found. AI engine is offline.")
            
        # Initialize the RAG searcher engine (unchanged — pgvector + SentenceTransformer)
        self.rag = RAGSearcher()

    def _build_context(self, query):
        """Perform semantic search to fetch relevant context chunks from pgvector."""
        results = self.rag.search(query, limit=5)
        if not results:
            return "No relevant knowledge base entries found for this query."
        
        context = "Here is the relevant verified knowledge base for Saint Paul University Surigao (SPUS):\n\n"
        for i, text in enumerate(results):
            context += f"- {text}\n"
        return context

    def process_query(self, user_message):
        """
        Takes the user message, retrieves RAG context, and generates a response via Groq.
        """
        if not self.client:
            return (
                "System Configuration Error: The AI brain is currently offline because "
                "the `GROQ_API_KEY` is missing in the `.env` file. "
                "Please configure it to enable intelligent responses."
            )
            
        msg = user_message.strip()
        if not msg:
            return "Please type a message."
        
        # Step 1: Retrieve context from the knowledge base (RAG)
        context = self._build_context(msg)
        
        # Step 2: Build the user message with embedded context
        user_content = (
            f"--- VERIFIED SPUS KNOWLEDGE ---\n"
            f"{context}\n"
            f"--- END KNOWLEDGE ---\n\n"
            f"Student Question: {msg}\n"
            f"Helpful Answer:"
        )
        
        # Step 3: Call Groq API with structured system + user messages
        try:
            chat_completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": PAULIBOT_SYSTEM_PROMPT},
                    {"role": "user", "content": user_content},
                ],
                temperature=0.6,       # Balanced: accurate but not robotic
                max_tokens=1024,        # Enough for detailed answers
                top_p=0.9,
                stream=False,
            )
            
            response_text = chat_completion.choices[0].message.content.strip()
            logger.info(f"Groq response generated successfully for query: '{msg[:50]}...'")
            return response_text
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Groq API error: {error_msg}")
            
            # User-friendly error messages
            if "rate_limit" in error_msg.lower() or "429" in error_msg:
                return (
                    "I'm receiving a lot of questions right now! 😅 "
                    "Please wait a moment and try again. "
                    "Maraming nagtatanong ngayon, subukan ulit mamaya!"
                )
            
            return (
                "I apologize, but I am currently experiencing technical difficulties "
                f"connecting to my intelligence network. ({error_msg})"
            )
