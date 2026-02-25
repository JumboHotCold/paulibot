import google.generativeai as genai
from django.conf import settings
from .rag import RAGSearcher

class PauliBotLogic:
    """
    Generative AI logic engine for PauliBot using Gemini API.
    Uses Phase 2 Retrieval-Augmented Generation (RAG) by fetching relevant FAQ context.
    """

    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None
            
        # Initialize the RAG searcher engine
        self.rag = RAGSearcher()

    def _build_context(self, query):
        """Perform semantic search to fetch relevant context chunks."""
        results = self.rag.search(query, limit=3)
        context = "Here is the relevant verified knowledge base for Saint Paul University Surigao (SPUS):\n\n"
        for i, text in enumerate(results):
            context += f"- {text}\n"
        return context

    def process_query(self, user_message):
        """
        Takes the user message, wraps it with context, and generates a response via Gemini.
        """
        if not self.model:
            return "System Configuration Error: The AI brain is currently offline because the `GEMINI_API_KEY` is missing in the `.env` file. Please configure it to enable intelligent responses."
            
        msg = user_message.strip()
        context = self._build_context(msg)
        
        prompt = (
            "You are PauliBot, the official, helpful, and friendly AI assistant for Saint Paul University Surigao (SPUS). "
            "Your goal is to provide accurate information based ONLY on the verified knowledge base provided below.\n\n"
            "GUIDELINES:\n"
            "1. Use ONLY the provided context to answer. Do not use outside knowledge.\n"
            "2. If the answer is found in the context, be thorough but concise.\n"
            "3. If the answer is NOT in the context, say exactly: \"I'm sorry, but I don't have that specific information in my current knowledge base for SPUS. For further assistance, please contact the university administration.\"\n"
            "4. Maintain a professional and academic tone.\n\n"
            f"--- VERIFIED SPUS KNOWLEDGE ---\n{context}\n--- END KNOWLEDGE ---\n\n"
            f"Student Question: {msg}\n"
            "Helpful Answer:"
        )
        
        try:
            response = self.model.generate_content(prompt)
            # Some responses from Gemini might have leading/trailing whitespace
            return response.text.strip()
        except Exception as e:
            # Handle rate limits, network errors, or API outages from Google gracefully
            return f"I apologize, but I am currently experiencing technical difficulties connecting to my intelligence network. ({str(e)})"
