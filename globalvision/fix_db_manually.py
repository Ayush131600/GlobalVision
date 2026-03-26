import os, django
from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "globalvision.settings")
django.setup()

def fix_db():
    with connection.cursor() as cursor:
        print("Checking table dashboard_blogpost...")
        try:
            # Check existing columns
            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='dashboard_blogpost'")
            columns = [row[0] for row in cursor.fetchall()]
            print(f"Current columns: {columns}")
            
            # Add missing columns
            if 'status' not in columns:
                print("Adding column 'status'...")
                cursor.execute("ALTER TABLE dashboard_blogpost ADD COLUMN status varchar(20) DEFAULT 'pending' NOT NULL")
            
            if 'rejection_reason' not in columns:
                print("Adding column 'rejection_reason'...")
                cursor.execute("ALTER TABLE dashboard_blogpost ADD COLUMN rejection_reason text")
            
            if 'admin_note' not in columns:
                print("Adding column 'admin_note'...")
                cursor.execute("ALTER TABLE dashboard_blogpost ADD COLUMN admin_note text")
                
            if 'updated_at' not in columns:
                print("Adding column 'updated_at'...")
                cursor.execute("ALTER TABLE dashboard_blogpost ADD COLUMN updated_at timestamptz DEFAULT now() NOT NULL")
            
            print("DB Fix Complete.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    fix_db()
