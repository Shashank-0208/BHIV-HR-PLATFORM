#!/usr/bin/env python3
"""
BHIV HR Platform - Database Restoration Script
Restores data from JSON backup to PostgreSQL database
Version: 1.0.0
"""

import os
import json
import psycopg2
from datetime import datetime
from typing import Any, Dict, List
import sys

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

def clear_table_data(cursor, table_name: str):
    """Clear all data from a table (but keep structure)"""
    # Disable triggers temporarily to avoid constraint issues
    cursor.execute(f"ALTER TABLE {table_name} DISABLE TRIGGER ALL")
    cursor.execute(f"DELETE FROM {table_name}")
    cursor.execute(f"ALTER TABLE {table_name} ENABLE TRIGGER ALL")

def insert_table_data(cursor, table_name: str, data: List[Dict[str, Any]]):
    """Insert data into a table"""
    if not data:
        print(f"[WARNING] {table_name}: No data to insert")
        return 0
    
    # Get column names from first record
    columns = list(data[0].keys())
    
    # Create placeholders for SQL
    placeholders = ', '.join(['%s'] * len(columns))
    columns_str = ', '.join([f'"{col}"' for col in columns])
    
    # Prepare SQL
    sql = f'INSERT INTO "{table_name}" ({columns_str}) VALUES ({placeholders})'
    
    # Prepare data rows
    rows = []
    for record in data:
        row = [record.get(col) for col in columns]
        rows.append(row)
    
    # Execute batch insert
    cursor.executemany(sql, rows)
    return len(rows)

def get_table_dependencies():
    """Define table insertion order based on foreign key dependencies"""
    # Tables with no dependencies first, then tables that depend on them
    return [
        'schema_version',
        'users',
        'clients', 
        'candidates',
        'jobs',
        'feedback',
        'interviews',
        'offers',
        'matching_cache',
        'audit_logs',
        'rate_limits',
        'csp_violations',
        'company_scoring_preferences',
        'job_applications',
        'workflows',
        'rl_predictions',
        'rl_feedback',
        'rl_model_performance',
        'rl_training_data'
    ]

def reset_sequences(cursor, table_name: str):
    """Reset auto-increment sequences for a table"""
    try:
        # Get the sequence name for the table's primary key
        cursor.execute(f"""
            SELECT pg_get_serial_sequence('{table_name}', 'id')
        """)
        result = cursor.fetchone()
        
        if result and result[0]:
            sequence_name = result[0]
            # Reset sequence to max ID + 1
            cursor.execute(f"""
                SELECT setval('{sequence_name}', 
                    COALESCE((SELECT MAX(id) FROM {table_name}), 1), 
                    true)
            """)
            print(f"[INFO] Reset sequence for {table_name}")
    except Exception as e:
        # Skip sequence reset for tables without id column (like schema_version)
        pass

def main():
    """Main restoration function"""
    backup_file = 'database_backup.json'
    
    if not os.path.exists(backup_file):
        print(f"[ERROR] Backup file not found: {backup_file}")
        return False
    
    try:
        # Load backup data
        print(f"[INFO] Loading backup from {backup_file}...")
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        metadata = backup_data.get('metadata', {})
        data = backup_data.get('data', {})
        
        print(f"[INFO] Backup info:")
        print(f"   Date: {metadata.get('extraction_date', 'Unknown')}")
        print(f"   Version: {metadata.get('version', 'Unknown')}")
        print(f"   Tables: {metadata.get('total_tables', 0)}")
        print(f"   Records: {metadata.get('total_records', 0)}")
        
        # Connect to database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print("\n[INFO] Starting database restoration...")
        
        # Get table insertion order
        table_order = get_table_dependencies()
        
        # Add any tables from backup that aren't in our predefined order
        backup_tables = set(data.keys())
        ordered_tables = set(table_order)
        missing_tables = backup_tables - ordered_tables
        if missing_tables:
            table_order.extend(sorted(missing_tables))
            print(f"[WARNING] Found additional tables: {', '.join(missing_tables)}")
        
        # Disable foreign key checks temporarily
        cursor.execute("SET session_replication_role = replica")
        
        total_restored = 0
        
        # Clear and restore each table
        for table_name in table_order:
            if table_name not in data:
                print(f"[WARNING] {table_name}: Not found in backup")
                continue
            
            try:
                table_data = data[table_name]
                
                # Clear existing data
                clear_table_data(cursor, table_name)
                
                # Insert new data
                records_inserted = insert_table_data(cursor, table_name, table_data)
                total_restored += records_inserted
                
                # Reset sequences
                reset_sequences(cursor, table_name)
                
                print(f"[OK] {table_name}: {records_inserted} records restored")
                
            except Exception as e:
                print(f"[ERROR] Error restoring {table_name}: {e}")
                continue
        
        # Re-enable foreign key checks
        cursor.execute("SET session_replication_role = DEFAULT")
        
        # Commit all changes
        conn.commit()
        
        print(f"\n[SUCCESS] Database restoration completed!")
        print(f"[INFO] Total records restored: {total_restored}")
        
        # Verify restoration
        cursor.execute("""
            SELECT table_name, 
                   (SELECT COUNT(*) FROM information_schema.tables t2 
                    WHERE t2.table_name = t1.table_name AND t2.table_schema = 'public') as exists
            FROM information_schema.tables t1
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """)
        
        tables_verified = cursor.fetchall()
        print(f"[OK] Verified {len(tables_verified)} tables exist")
        
    except Exception as e:
        print(f"[ERROR] Database restoration failed: {e}")
        if 'conn' in locals():
            conn.rollback()
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