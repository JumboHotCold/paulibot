"""
Management command to seed the Knowledge Base tables from the legacy data.py file.
This migrates the hardcoded data into the PostgreSQL database so Faculty can manage it.
"""
from django.core.management.base import BaseCommand
from chatbot.models import Location, StaffMember, FAQ
from chatbot.data import LOCATIONS, STAFF, ADMISSIONS_FAQ


class Command(BaseCommand):
    help = 'Seed the Knowledge Base tables with initial data from data.py'

    def handle(self, *args, **options):
        self.stdout.write("Seeding Knowledge Base...")

        # Seed Locations
        for key, data in LOCATIONS.items():
            obj, created = Location.objects.get_or_create(
                name=data['name'],
                defaults={
                    'description': data['description'],
                    'map_available': data.get('map_available', False),
                }
            )
            status = "CREATED" if created else "EXISTS"
            self.stdout.write(f"  [{status}] Location: {obj.name}")

        # Seed Staff
        for key, data in STAFF.items():
            obj, created = StaffMember.objects.get_or_create(
                name=data['name'],
                defaults={
                    'position': data['position'],
                    'office': data['office'],
                }
            )
            status = "CREATED" if created else "EXISTS"
            self.stdout.write(f"  [{status}] Staff: {obj.name}")

        # Seed FAQs
        for key, text in ADMISSIONS_FAQ.items():
            obj, created = FAQ.objects.get_or_create(
                category=key.capitalize(),
                defaults={
                    'question': f"What is the {key} information?",
                    'answer': text,
                }
            )
            status = "CREATED" if created else "EXISTS"
            self.stdout.write(f"  [{status}] FAQ: {obj.category}")

        self.stdout.write(self.style.SUCCESS("\nKnowledge Base seeded successfully!"))
