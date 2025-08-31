import sqlite3 as sq

def init_database():
    conn = sq.connect("journal.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entries(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        category TEXT DEFAULT "journal",
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                   )
                   """)
    
    conn.commit()
    conn.close()
    print("Database Initialized")

def new_entry(content, category):
    conn = sq.connect("journal.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO entries(content, category)
        VALUES(?,?)
                   """, (content, category))
    
    entry_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return entry_id

def get_entries():
    conn = sq.connect("journal.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, content, category, timestamp
        FROM entries
        ORDER BY timestamp DESC
        """
    )

    response = cursor.fetchall()
    conn.close()
    return [
        {
            "id": row[0],
            "content": row[1],
            "category": row[2],
            "timestamp": row[3]
        } for row in response
    ]
    