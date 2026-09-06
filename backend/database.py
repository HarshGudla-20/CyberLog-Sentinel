import sqlite3


DATABASE_NAME = "cyberlog.db"


def create_database():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS security_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ip_address TEXT,
            event_type TEXT,
            failed_attempts INTEGER,
            risk_level TEXT,
            raw_log TEXT
        )
    """)

    connection.commit()
    connection.close()


def insert_event(event):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    # Check if the same threat already exists
    cursor.execute("""
        SELECT id
        FROM security_events
        WHERE ip_address = ?
        AND event_type = ?
        AND failed_attempts = ?
    """, (
        event.get("ip_address"),
        event.get("event_type"),
        event.get("failed_attempts", 0)
    ))

    existing_event = cursor.fetchone()

    # Insert only if it does not already exist
    if existing_event is None:

        cursor.execute("""
            INSERT INTO security_events
            (timestamp, ip_address, event_type, failed_attempts, risk_level, raw_log)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            event.get("timestamp"),
            event.get("ip_address"),
            event.get("event_type"),
            event.get("failed_attempts", 0),
            event.get("risk_level", "LOW"),
            event.get("raw_log", "")
        ))

        connection.commit()

    connection.close()


def get_all_events():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM security_events
        ORDER BY id DESC
    """)

    events = cursor.fetchall()

    connection.close()

    return events


if __name__ == "__main__":

    create_database()

    print("Database created successfully!")