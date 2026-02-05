#!/usr/bin/env python3
"""
Create a valid API key for testing
"""
import sys
sys.path.insert(0, 'server')
import sqlite3
import uuid

print("=" * 70)
print("SETTING UP TEST API KEY")
print("=" * 70)

try:
    # Connect to database
    db_path = 'sqlite.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='api_keys'")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        print("\n✗ Database not initialized - creating tables...")
        
        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL UNIQUE,
                owner TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS request_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                api_key_id INTEGER REFERENCES api_keys(id),
                language TEXT NOT NULL,
                classification TEXT NOT NULL,
                confidence_score REAL NOT NULL,
                explanation TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                client_ip TEXT
            )
        """)
        
        print("✓ Tables created")
    else:
        print("\n✓ Database tables exist")
    
    # Check if test key exists
    cursor.execute("SELECT id, key FROM api_keys WHERE key = 'sk_test_123456789'")
    existing = cursor.fetchone()
    
    if existing:
        print(f"✓ Test API key already exists (ID: {existing[0]})")
    else:
        # Create test key
        test_key = 'sk_test_123456789'
        cursor.execute(
            "INSERT INTO api_keys (key, owner, is_active) VALUES (?, ?, ?)",
            (test_key, 'Test User', 1)
        )
        conn.commit()
        print(f"✓ Created test API key: {test_key}")
    
    # List all API keys
    print("\n✓ Available API keys:")
    cursor.execute("SELECT id, key, owner, is_active FROM api_keys")
    keys = cursor.fetchall()
    for key_id, key, owner, is_active in keys:
        status = "ACTIVE" if is_active else "INACTIVE"
        print(f"  - {key} ({owner}) [{status}]")
    
    conn.close()
    print("\n✓ Setup complete")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("=" * 70)
