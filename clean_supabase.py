"""
Clean all records from Supabase database
WARNING: This will delete ALL data!
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("ERROR: DATABASE_URL not found in .env file")
    exit(1)

print("Connecting to Supabase...")
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        print("\nWARNING: This will delete ALL data from the database!")
        print("Tables to be cleaned:")
        print("  - messages")
        print("  - favorability_tracking")
        print("  - line_user_mappings")
        print("  - characters")
        print("  - user_preferences")
        print("  - users")

        confirm = input("\nType 'DELETE ALL' to confirm: ")

        if confirm != "DELETE ALL":
            print("Cancelled. No data was deleted.")
            exit(0)

        print("\nDeleting all records...")

        # Delete in order to respect foreign key constraints
        conn.execute(text("DELETE FROM messages"))
        print("Deleted all messages")

        conn.execute(text("DELETE FROM favorability_tracking"))
        print("Deleted all favorability tracking")

        conn.execute(text("DELETE FROM line_user_mappings"))
        print("Deleted all LINE user mappings")

        conn.execute(text("DELETE FROM user_preferences"))
        print("Deleted all user preferences")

        conn.execute(text("DELETE FROM characters"))
        print("Deleted all characters")

        conn.execute(text("DELETE FROM users"))
        print("Deleted all users")

        conn.commit()

        print("\nDatabase cleaned successfully!")
        print("You can now start fresh with new characters.")

except Exception as e:
    print(f"\nError: {e}")
    exit(1)
