import requests
from .models import TechnicalCompliance


def run_pipeline(keyword=None):
    url = "https://www.federalregister.gov/api/v1/documents.json"

    params = {
        'per_page': 100,
        'order': 'newest',
    }

    if keyword:
        params['conditions[term]'] = keyword

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        results = data.get('results', [])
    except Exception as e:
        print(f"Error fetching data from Federal Register API: {e}")
        return []

    newly_created_docs = []

    for item in results:
        html_url = item.get('html_url', '')
        if not html_url:
            continue

        title = item.get('title', 'Untitled')
        abstract = item.get('abstract', '') or ''
        pub_date = item.get('publication_date')

        # ✅ Uses html_url as the unique identifier field on TechnicalCompliance
        doc, created = TechnicalCompliance.objects.update_or_create(
            html_url=html_url,
            defaults={
                'title': title,
                'abstract': abstract,
                'publication_date': pub_date,
            }
        )

        if created:
            newly_created_docs.append(doc)

    return newly_created_docs