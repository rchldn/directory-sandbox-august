

import sqlite3

def create_database():
    conn = sqlite3.connect('musicians.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS musicians (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        genre TEXT NOT NULL,
        instrument TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
    ''')
    
    conn.commit()
    conn.close()

create_database()
