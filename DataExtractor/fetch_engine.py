import requests


def fetch_compliance_data():
    # Example using the open US Federal Register API to track manufacturing/technical rule updates
    url = "https://www.federalregister.gov/api/v1/documents.json"

    # We query for specific technical keywords like 'manufacturing' or 'specifications'
    params = {
        "conditions[term]": "manufacturing engineering",
        "per_page": 5
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Automatically triggers an error if the site is down
        return response.json()  # Returns a clean Python dictionary
    except requests.exceptions.RequestException as e:
        print(f"Pipeline Error: {e}")
        return None


# Test the engine
if __name__ == "__main__":
    data = fetch_compliance_data()
    if data:
        print("Successfully connected and fetched data payload!")
        # Print the title of the first document found
        print(f"Sample Entry: {data['results'][0]['title']}")
