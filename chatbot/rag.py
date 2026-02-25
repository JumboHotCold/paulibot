"""
PauliBot RAG (Retrieval-Augmented Generation) Engine
=====================================================
Phase 2: Database-backed vector search using PostgreSQL + pgvector.

This module reads knowledge from the database (Location, StaffMember, FAQ),
generates embeddings, and performs semantic search against pgvector.
"""
import logging
from sentence_transformers import SentenceTransformer
from pgvector.django import L2Distance

logger = logging.getLogger(__name__)


class RAGSearcher:
    """Manages semantic search using PostgreSQL pgvector."""

    def __init__(self):
        logger.info("Initializing RAG Searcher (pgvector mode)...")
        logger.info("Loading embedding model (all-MiniLM-L6-v2)...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        logger.info("RAG Searcher ready.")

    def _generate_embedding(self, text):
        """Generate a 384-dimension embedding for a text string."""
        return self.model.encode(text).tolist()

    def ensure_embeddings(self):
        """
        Generate embeddings for any Knowledge Base entries that don't have one yet.
        Called when a staff member adds new data via the admin panel.
        """
        from chatbot.models import Location, StaffMember, FAQ

        updated = 0

        for loc in Location.objects.filter(embedding__isnull=True):
            text = f"Location: {loc.name}. {loc.description}"
            loc.embedding = self._generate_embedding(text)
            loc.save(update_fields=['embedding'])
            updated += 1

        for staff in StaffMember.objects.filter(embedding__isnull=True):
            text = f"Staff: {staff.name}, {staff.position}. Office located at {staff.office}."
            staff.embedding = self._generate_embedding(text)
            staff.save(update_fields=['embedding'])
            updated += 1

        for faq in FAQ.objects.filter(embedding__isnull=True):
            text = f"FAQ about {faq.category}: {faq.question} - {faq.answer}"
            faq.embedding = self._generate_embedding(text)
            faq.save(update_fields=['embedding'])
            updated += 1

        if updated:
            logger.info(f"Generated embeddings for {updated} new knowledge entries.")

    def search(self, query, limit=3):
        """
        Perform semantic vector search across all Knowledge Base tables.
        Returns the top matching text chunks ordered by actual L2 distance.
        """
        from chatbot.models import Location, StaffMember, FAQ
        from pgvector.django import L2Distance

        # Ensure all entries have embeddings before searching
        self.ensure_embeddings()

        query_vector = self._generate_embedding(query)
        all_results = []

        # Search Locations
        locations = Location.objects.exclude(embedding__isnull=True).annotate(
            distance=L2Distance('embedding', query_vector)
        ).order_by('distance')[:limit]
        
        for loc in locations:
            all_results.append({
                'text': f"Location: {loc.name}. {loc.description}",
                'distance': loc.distance
            })

        # Search Staff
        staff_members = StaffMember.objects.exclude(embedding__isnull=True).annotate(
            distance=L2Distance('embedding', query_vector)
        ).order_by('distance')[:limit]
        
        for staff in staff_members:
            all_results.append({
                'text': f"Staff: {staff.name}, {staff.position}. Office located at {staff.office}.",
                'distance': staff.distance
            })

        # Search FAQs
        faqs = FAQ.objects.exclude(embedding__isnull=True).annotate(
            distance=L2Distance('embedding', query_vector)
        ).order_by('distance')[:limit]
        
        for faq in faqs:
            all_results.append({
                'text': f"FAQ about {faq.category}: {faq.question} - {faq.answer}",
                'distance': faq.distance
            })

        # Sort all results by distance and pick the top `limit`
        all_results.sort(key=lambda x: x['distance'])
        
        final_results = [r['text'] for r in all_results[:limit]]
        logger.info(f"Top RAG results for query '{query}': {final_results}")
        return final_results
