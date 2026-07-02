import requests
from .models import TechnicalCompliance
from datetime import datetime, timedelta


def run_federal_register_pipeline(keywords):
    # 1. Look for documents published in the last 30 days
    time_delta = datetime.now() - timedelta(days=30)
    formatted_date = time_delta.strftime('%Y-%m-%d')

    # Federal Register API Endpoint
    url = "https://www.federalregister.gov/api/v1/documents.json"
    current_run_timestamp = datetime.now()

    for keyword in keywords:
        clean_keyword = keyword.strip()
        if not clean_keyword:
            continue

        params = {
            'conditions[term]': clean_keyword,
            'conditions[publication_date][gte]': formatted_date,
            'per_page': 100
        }

        try:
            response = requests.get(url, params=params)
            if response.status_code != 200:
                print(f"API Error: {response.status_code}")
                continue

            data = response.json()
            results = data.get('results', [])

            for doc in results:
                # FIX: We use title to match existing docs instead of hijacking the numeric id column
                TechnicalCompliance.objects.update_or_create(
                    title=doc.get('title', ''),
                    defaults={
                        'abstract': doc.get('abstract', '') or '',
                        'publication_date': doc.get('publication_date'),
                        'html_url': doc.get('html_url', ''),
                        'added_at': current_run_timestamp
                    }
                )
        except Exception as e:
            print(f"Error processing keyword {clean_keyword}: {e}")
            continue