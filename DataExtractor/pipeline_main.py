import sqlite3
from fetch_engine import fetch_compliance_data
from database_manager import init_database


def run_pipeline():
    # 1. Ensure database is ready
    init_database()

    # 2. Fetch live data
    print("Ingesting live data feed...")
    payload = fetch_compliance_data()

    if not payload or 'results' not in payload:
        print("No valid data to process.")
        return

    # 3. Process and Transform data
    conn = sqlite3.connect("compliance_tracker.db")
    cursor = conn.cursor()

    records_updated = 0

    for item in payload['results']:
        # Extracting specific data fields safely (using .get() to prevent missing key errors)
        doc_id = item.get('document_number')
        title = item.get('title')
        pub_date = item.get('publication_date')
        doc_type = item.get('type')
        abstract = item.get('abstract', 'No description provided.')

        # 4. Load into Database (Upsert pattern)
        cursor.execute("""
            INSERT OR REPLACE INTO technical_compliance 
            (document_id, title, publication_date, type, abstract)
            VALUES (?, ?, ?, ?, ?)
        """, (doc_id, title, pub_date, doc_type, abstract))

        records_updated += 1

    conn.commit()
    conn.close()
    print(f"Pipeline complete. Processed and secured {records_updated} records.")


if __name__ == "__main__":
    run_pipeline()