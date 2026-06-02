import sqlite3


def init_database():
    # Connects to database file (creates it if it doesn't exist)
    conn = sqlite3.connect("compliance_tracker.db")
    cursor = conn.cursor()

    # Create a table to store our technical updates safely
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS technical_compliance (
            document_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            publication_date TEXT,
            type TEXT,
            abstract TEXT,
            last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print("Local database initialized successfully with structured schemas.")


if __name__ == "__main__":
    init_database()