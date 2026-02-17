import re
from .data import LOCATIONS, STAFF, ADMISSIONS_FAQ

class PauliBotLogic:
    """
    Deterministic logic engine for PauliBot.
    Strictly follows formatted output rules.
    """

    def process_query(self, user_message):
        """
        Analyzes the message and returns the appropriate structured response.
        """
        msg = user_message.lower().strip()
        
        # 1. SCOPE CHECK
        # Simple keywords to detect general greetings vs off-topic
        # If it's a greeting, we can answer generally, but if it's clearly unrelated...
        # For MVP, we will assume everything is relevant unless it matches specific off-topic triggers
        # or if we fail to match any known intent? 
        # Actually, the prompt says "If a question is outside this scope...".
        # Let's try to match intents first. If no intent is found, we might default to "Unclear" or "Out of Scope" depending on the input.
        
        # OFF-TOPIC filter (Basic examples)
        off_topic_keywords = ['cooking', 'recipe', 'movie', 'game', 'weather', 'basketball', 'nba', 'president of usa']
        if any(word in msg for word in off_topic_keywords):
            return "I’m sorry, I can only assist with inquiries related to Saint Paul University Surigao."

        # 2. INTENT: LOCATION
        location_match = self._check_location(msg)
        if location_match:
            return location_match

        # 3. INTENT: STAFF
        staff_match = self._check_staff(msg)
        if staff_match:
            return staff_match

        # 4. INTENT: GENERAL INFO
        general_match = self._check_general(msg)
        if general_match:
            return general_match
            
        # 5. GREETINGS (Safety fallback for politeness)
        if msg in ['hi', 'hello', 'good morning', 'good afternoon']:
             return "GENERAL INFORMATION:\nHello! I am PauliBot. Ask me about admissions, locations, or staff at SPUS."

        # 6. FALLBACK -> Unclear / Out of Scope
        # If we really don't know what they are talking about, we ask for clarification.
        return "Could you please clarify your question so I can assist you better?"

    def _check_location(self, msg):
        """Checks for location-based queries."""
        if 'where' not in msg and 'location' not in msg and 'find' not in msg:
            return None
            
        for key, data in LOCATIONS.items():
            if key in msg or data['name'].lower() in msg:
                return (
                    "LOCATION:\n"
                    f"Name: {data['name']}\n"
                    f"Description: {data['description']}\n"
                    f"Map Available: {'Yes' if data['map_available'] else 'No'}"
                )
        return None

    def _check_staff(self, msg):
        """Checks for staff-based queries."""
        if 'who' not in msg and 'head' not in msg and 'president' not in msg and 'dean' not in msg:
            return None
            
        # Check specific roles first
        if 'president' in msg:
            data = STAFF['president']
            return self._format_staff(data)
        if 'vp' in msg or 'vice' in msg:
            data = STAFF['vp_academics']
            return self._format_staff(data)
        if 'dean' in msg and 'cics' in msg:
            data = STAFF['dean_cics']
            return self._format_staff(data)
            
        return None

    def _format_staff(self, data):
        return (
            "STAFF INFORMATION:\n"
            f"Name: {data['name']}\n"
            f"Position: {data['position']}\n"
            f"Office/Location: {data['office']}"
        )

    def _check_general(self, msg):
        """Checks for admission/enrollment/general queries."""
        # Enrollment
        if 'enroll' in msg or 'registration' in msg:
            return f"GENERAL INFORMATION:\n{ADMISSIONS_FAQ['enrollment']}"
        
        # Tuition
        if 'tuition' in msg or 'fee' in msg or 'cost' in msg:
            return f"GENERAL INFORMATION:\n{ADMISSIONS_FAQ['tuition']}"
            
        # Courses
        if 'course' in msg or 'program' in msg or 'offer' in msg:
            return f"GENERAL INFORMATION:\n{ADMISSIONS_FAQ['courses']}"

        # Scholarships
        if 'scholarship' in msg or 'aid' in msg:
            return f"GENERAL INFORMATION:\n{ADMISSIONS_FAQ['scholarship']}"
            
        return None
