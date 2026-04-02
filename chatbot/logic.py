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
            "LANGUAGE GUIDELINES (VERY IMPORTANT):\n"
            "- Detect the language of the CURRENT message ONLY. Ignore any previous conversation language.\n"
            "- If THIS message is in Filipino, respond entirely in Filipino.\n"
            "- If THIS message is in English, respond entirely in English.\n"
            "- If THIS message mixes Filipino and English (Taglish), respond in Taglish.\n"
            "- The student may switch languages between messages. ALWAYS match the language of their CURRENT message.\n"
            "- Always keep a warm, friendly, and approachable tone — like a helpful campus guide.\n\n"
            "GREETING & CASUAL CHAT GUIDELINES:\n"
            "- If the student sends a greeting (e.g., 'hi', 'hello', 'kamusta', 'hey', 'good morning', 'magandang umaga'), "
            "respond with a friendly greeting in the SAME language and introduce yourself as PauliBot. "
            "Then offer to help with SPUS-related questions. Do NOT say you don't have information — greetings are not knowledge-base queries.\n"
            "- If the student asks casual questions like 'how are you?', 'kamusta ka?', 'what's up?', "
            "respond warmly and naturally (e.g., 'I'm doing great, ready to help you!' or 'Mabuti naman! Ano ang maitutulong ko?'). "
            "These are social interactions, NOT knowledge-base lookups.\n\n"
            "ANSWER GUIDELINES:\n"
            "1. For SPUS-related questions, use ONLY the provided context to answer. Do not use outside knowledge.\n"
            "2. If the answer is found in the context, be thorough but concise.\n"
            "3. If the student asks an SPUS-related question and the answer is NOT in the context, say: "
            "\"I'm sorry, but I don't have that specific information in my current knowledge base for SPUS. "
            "For further assistance, please contact the university administration.\" (Respond in the student's language.)\n"
            "4. Maintain a professional and academic tone.\n\n"
            "FOLLOW-UP SUGGESTIONS:\n"
            "After your answer, ALWAYS provide exactly 3 short follow-up questions the student might want to ask next. "
            "Write them on the LAST line of your response in this EXACT format:\n"
            "[SUGGESTIONS: \"Question 1?\" | \"Question 2?\" | \"Question 3?\"]\n"
            "The suggestions must be in the SAME language as your response and relevant to SPUS topics.\n\n"
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
