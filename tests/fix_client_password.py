#!/usr/bin/env python3
"""
Fix client password hash for TECH001
"""

import psycopg2
import bcrypt

# Database connection
DATABASE_URL = "postgresql://bhiv_user:8oaleQyxSfBJp7uqt0UJoAXnOhPj63nG@dpg-d40c0kf5r7bs73abt080-a.oregon-postgres.render.com/bhiv_hr_jcuu_w5fl"

def fix_client_password():
    """Fix client password hash"""
    print("Fixing Client Password Hash")
    print("=" * 30)
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Generate proper password hash for "demo123"
        password = "demo123"
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        print(f"Generated hash for '{password}': {password_hash[:50]}...")
        
        # Update the password hash
        cursor.execute("""
            UPDATE clients 
            SET password_hash = %s
            WHERE client_id = %s
        """, (password_hash, "TECH001"))
        
        conn.commit()
        
        # Verify the update
        cursor.execute("""
            SELECT client_id, password_hash
            FROM clients WHERE client_id = %s
        """, ("TECH001",))
        
        client = cursor.fetchone()
        
        if client and client[1]:
            # Test the password verification
            stored_hash = client[1]
            is_valid = bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
            
            print(f"Client: {client[0]}")
            print(f"Password hash updated: Yes")
            print(f"Password verification test: {'PASS' if is_valid else 'FAIL'}")
            
            if is_valid:
                print("\nSUCCESS: Client password fixed")
                return True
            else:
                print("\nFAIL: Password verification failed")
                return False
        else:
            print("FAIL: Client not found or password not updated")
            return False
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"FAIL: Password fix error: {e}")
        return False

if __name__ == "__main__":
    fix_client_password()
