#!/usr/bin/env python3
"""
Query database to see recent API results
"""
import sqlite3
import json
from datetime import datetime, timedelta

print("=" * 80)
print("QUERY REQUEST_LOGS TABLE")
print("=" * 80)

try:
    conn = sqlite3.connect('sqlite.db')
    cursor = conn.cursor()
    
    # Get recent requests (last 10)
    cursor.execute("""
        SELECT 
            id, 
            language, 
            classification, 
            confidence_score, 
            explanation, 
            timestamp
        FROM request_logs
        ORDER BY id DESC
        LIMIT 15
    """)
    
    results = cursor.fetchall()
    
    print(f"\nTotal results: {len(results)}\n")
    
    for row in results:
        rid, language, classification, confidence, explanation, timestamp = row
        print(f"ID: {rid}")
        print(f"  Language: {language}")
        print(f"  Classification: {classification}")
        print(f"  Confidence: {confidence:.2%}")
        print(f"  Explanation: {explanation[:70]}...")
        print(f"  Timestamp: {timestamp}")
        print()
    
    # Get statistics
    cursor.execute("""
        SELECT 
            classification,
            COUNT(*) as count,
            AVG(confidence_score) as avg_confidence
        FROM request_logs
        GROUP BY classification
    """)
    
    print("\n" + "=" * 80)
    print("STATISTICS")
    print("=" * 80 + "\n")
    
    for classification, count, avg_conf in cursor.fetchall():
        print(f"{classification:20s}: {count:3d} requests, Avg Confidence: {avg_conf:.2%}")
    
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
