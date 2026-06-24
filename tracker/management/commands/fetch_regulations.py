import requests
from django.core.management.base import BaseCommand
from tracker.models import TechnicalCompliance


class Command(BaseCommand):
    help = 'Fetches data from the Federal Register API and saves it to the database'

    def handle(self, *args, **options):
        self.stdout.write("Starting API data fetch...")

        # 1. Define your API endpoint and parameters (Use your working API parameters here)
        url = "https://www.federalregister.gov/api/v1/documents.json"
        params = {
            "conditions[term][]": "manufacturing engineering",  # Change this to your exact search keyword
            "per_page": 50
        }

        # 2. Hit the API
        response = requests.get(url, params=params)
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f"Failed to fetch data. Status code: {response.status_code}"))
            return

        data = response.json()
        results = data.get("results", [])

        count = 0
        # 3. Loop through your items and run the Django UPSERT logic
        for doc in results:
            # We look up the record using the unique key
            document_number = doc.get("document_number")

            if not document_number:
                continue

            # update_or_create takes defaults= for the values you want to update/insert
            obj, created = TechnicalCompliance.objects.update_or_create(
                document_number=document_number,
                defaults={
                    "title": doc.get("title", "No Title"),
                    "publication_date": doc.get("publication_date"),
                    "html_url": doc.get("html_url", ""),
                    "abstract": doc.get("abstract", "")
                }
            )

            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully processed records. Added {count} new entries!"))