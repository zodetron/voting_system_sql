import sqlite3

def init_database():
    conn = sqlite3.connect('voting_system.db')
    cursor = conn.cursor()
    
    # Create candidates table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            party TEXT NOT NULL,
            votes INTEGER DEFAULT 0
        )
    ''')
    
    # Create voters table to prevent duplicate voting
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS voters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            voter_id TEXT UNIQUE NOT NULL,
            has_voted BOOLEAN DEFAULT FALSE
        )
    ''')
    
    # Insert sample candidates
    candidates = [
        ('John Smith', 'Democratic Party', 0),
        ('Sarah Johnson', 'Republican Party', 0),
        ('Mike Chen', 'Green Party', 0),
        ('Lisa Rodriguez', 'Independent', 0)
    ]
    
    cursor.executemany('INSERT INTO candidates (name, party, votes) VALUES (?, ?, ?)', candidates)
    
    # Insert sample voters
    voters = [
        ('V001', False),
        ('V002', False),
        ('V003', False),
        ('V004', False),
        ('V005', False)
    ]
    
    cursor.executemany('INSERT INTO voters (voter_id, has_voted) VALUES (?, ?)', voters)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_database()