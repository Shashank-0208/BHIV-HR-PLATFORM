#!/usr/bin/env python3
"""
BHIV HR Platform - Database Extraction Script
Extracts all data from PostgreSQL database and saves to JSON files
Version: 1.0.0
"""

import os
import json
import psycopg2
from datetime import datetime, date
import decimal
from typing import Any, Dict, List

class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder for datetime and decimal objects"""
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        return super().default(obj)

def get_db_connection():
    """Get database connection from environment variables"""
    db_config = {
        'host': os.getenv('DB_HOST', '127.0.0.1'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': os.getenv('POSTGRES_DB', 'bhiv_hr'),
        'user': os.getenv('POSTGRES_USER', 'bhiv_user'),
        'password': os.getenv('POSTGRES_PASSWORD', 'your_password_here')
    }
    
    # Try DATABASE_URL first (production format)
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        return psycopg2.connect(database_url)
    
    return psycopg2.connect(**db_config)

def extract_table_data(cursor, table_name: str) -> List[Dict[str, Any]]:
    """Extract all data from a table"""
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    
    return [dict(zip(columns, row)) for row in rows]

def get_all_tables(cursor) -> List[str]:
    """Get list of all tables in the database"""
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE'
        ORDER BY table_name
    """)
    return [row[0] for row in cursor.fetchall()]

def main():
    """Main extraction function"""
    try:
        # Connect to database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print("[INFO] Starting database extraction...")
        
        # Get all tables
        tables = get_all_tables(cursor)
        print(f"[INFO] Found {len(tables)} tables: {', '.join(tables)}")
        
        # Extract data from all tables
        all_data = {}
        total_records = 0
        
        for table in tables:
            try:
                data = extract_table_data(cursor, table)
                all_data[table] = data
                record_count = len(data)
                total_records += record_count
                print(f"[OK] {table}: {record_count} records")
            except Exception as e:
                print(f"[ERROR] Error extracting {table}: {e}")
                all_data[table] = []
        
        # Add metadata
        extraction_info = {
            'extraction_date': datetime.now().isoformat(),
            'database_name': os.getenv('POSTGRES_DB', 'bhiv_hr'),
            'total_tables': len(tables),
            'total_records': total_records,
            'tables': list(tables),
            'version': '4.3.1'
        }
        
        # Save to JSON file
        output_file = 'database_backup.json'
        backup_data = {
            'metadata': extraction_info,
            'data': all_data
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, cls=DateTimeEncoder, indent=2, ensure_ascii=False)
        
        print(f"\n[SUCCESS] Database extraction completed!")
        print(f"[INFO] File: {output_file}")
        print(f"[INFO] Total records: {total_records}")
        print(f"[INFO] Tables: {len(tables)}")
        
        # Show file size
        file_size = os.path.getsize(output_file)
        print(f"[INFO] File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
        
    except Exception as e:
        print(f"[ERROR] Database extraction failed: {e}")
        return False
    
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)