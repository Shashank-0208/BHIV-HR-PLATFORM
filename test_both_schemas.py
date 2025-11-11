#!/usr/bin/env python3
"""
Test both production_ready_schema.sql and consolidated_schema.sql
Honest comparison and assessment
"""
import os
import psycopg2
from datetime import datetime

DATABASE_URL = "postgresql://bhiv_user:8oaleQyxSfBJp7uqt0UJoAXnOhPj63nG@dpg-d40c0kf5r7bs73abt080-a.oregon-postgres.render.com/bhiv_hr_jcuu_w5fl"

def analyze_schema_file(filepath):
    """Analyze schema file content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count key components
        tables = content.count('CREATE TABLE')
        indexes = content.count('CREATE INDEX')
        triggers = content.count('CREATE TRIGGER')
        extensions = content.count('CREATE EXTENSION')
        functions = content.count('CREATE OR REPLACE FUNCTION')
        
        # Check for specific features
        has_extensions = 'uuid-ossp' in content and 'pg_trgm' in content
        has_job_applications = 'job_applications' in content
        has_auth_columns = 'failed_login_attempts' in content
        has_sample_data = 'INSERT INTO' in content
        
        return {
            'tables': tables,
            'indexes': indexes,
            'triggers': triggers,
            'extensions': extensions,
            'functions': functions,
            'has_extensions': has_extensions,
            'has_job_applications': has_job_applications,
            'has_auth_columns': has_auth_columns,
            'has_sample_data': has_sample_data,
            'file_size': len(content),
            'lines': len(content.split('\n'))
        }
    except Exception as e:
        return {'error': str(e)}

def test_current_production():
    """Test current production database state"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Count tables
        cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE'")
        table_count = cur.fetchone()[0]
        
        # Count indexes
        cur.execute("SELECT COUNT(*) FROM pg_indexes WHERE schemaname = 'public' AND indexname LIKE 'idx_%'")
        index_count = cur.fetchone()[0]
        
        # Check extensions
        cur.execute("SELECT COUNT(*) FROM pg_extension WHERE extname IN ('uuid-ossp', 'pg_stat_statements', 'pg_trgm')")
        extension_count = cur.fetchone()[0]
        
        # Check schema version
        cur.execute("SELECT version FROM schema_version ORDER BY applied_at DESC LIMIT 1")
        version = cur.fetchone()[0] if cur.fetchone() else "unknown"
        
        cur.close()
        conn.close()
        
        return {
            'tables': table_count,
            'indexes': index_count,
            'extensions': extension_count,
            'version': version
        }
    except Exception as e:
        return {'error': str(e)}

def main():
    print("TESTING BOTH SCHEMA FILES")
    print("=" * 50)
    
    # Test production_ready_schema.sql
    print("\n1. PRODUCTION_READY_SCHEMA.SQL ANALYSIS")
    prod_ready = analyze_schema_file('services/db/production_ready_schema.sql')
    
    # Test consolidated_schema.sql  
    print("\n2. CONSOLIDATED_SCHEMA.SQL ANALYSIS")
    consolidated = analyze_schema_file('services/db/consolidated_schema.sql')
    
    # Test current production state
    print("\n3. CURRENT PRODUCTION DATABASE STATE")
    current_prod = test_current_production()
    
    # Comparison
    print("\n" + "=" * 50)
    print("HONEST COMPARISON RESULTS")
    print("=" * 50)
    
    print(f"\n[FILE ANALYSIS]")
    print(f"Production Ready Schema:")
    if 'error' not in prod_ready:
        print(f"  Tables: {prod_ready['tables']}")
        print(f"  Indexes: {prod_ready['indexes']}")
        print(f"  Extensions: {prod_ready['extensions']}")
        print(f"  Has Extensions: {prod_ready['has_extensions']}")
        print(f"  Has Job Applications: {prod_ready['has_job_applications']}")
        print(f"  Has Auth Columns: {prod_ready['has_auth_columns']}")
        print(f"  File Size: {prod_ready['file_size']} chars")
    else:
        print(f"  ERROR: {prod_ready['error']}")
    
    print(f"\nConsolidated Schema:")
    if 'error' not in consolidated:
        print(f"  Tables: {consolidated['tables']}")
        print(f"  Indexes: {consolidated['indexes']}")
        print(f"  Extensions: {consolidated['extensions']}")
        print(f"  Has Extensions: {consolidated['has_extensions']}")
        print(f"  Has Job Applications: {consolidated['has_job_applications']}")
        print(f"  Has Auth Columns: {consolidated['has_auth_columns']}")
        print(f"  File Size: {consolidated['file_size']} chars")
    else:
        print(f"  ERROR: {consolidated['error']}")
    
    print(f"\n[PRODUCTION DATABASE STATE]")
    if 'error' not in current_prod:
        print(f"  Tables: {current_prod['tables']}")
        print(f"  Indexes: {current_prod['indexes']}")
        print(f"  Extensions: {current_prod['extensions']}/3")
        print(f"  Version: {current_prod['version']}")
    else:
        print(f"  ERROR: {current_prod['error']}")
    
    # Honest assessment
    print(f"\n[HONEST ASSESSMENT]")
    
    if 'error' not in prod_ready and 'error' not in consolidated:
        if prod_ready['tables'] < consolidated['tables']:
            print("  [ISSUE] Production Ready schema is INCOMPLETE - missing tables")
        elif prod_ready['has_extensions'] and not consolidated['has_extensions']:
            print("  [ADVANTAGE] Production Ready has extensions, Consolidated missing")
        elif consolidated['has_extensions'] and prod_ready['has_extensions']:
            print("  [EQUAL] Both have extensions")
        else:
            print("  [ISSUE] Neither has proper extensions")
    
    print(f"\n[RECOMMENDATION]")
    if 'error' not in consolidated and consolidated['tables'] > 4:
        print("  [ACTION] Update consolidated_schema.sql with extensions")
        print("  [REASON] Consolidated is complete, just needs extensions")
    else:
        print("  [ACTION] Use production_ready_schema.sql")
        print("  [REASON] More reliable for new deployments")

if __name__ == "__main__":
    main()