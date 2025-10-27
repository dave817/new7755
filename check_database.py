"""Quick script to check database state"""
from backend.database import SessionLocal, Character, LineUserMapping, User

db = SessionLocal()

# Check characters
chars = db.query(Character).all()
print(f"\n✅ Total Characters: {len(chars)}")
for char in chars:
    print(f"   - ID: {char.character_id}, Name: {char.name}, Gender: {char.gender}")

# Check users
users = db.query(User).all()
print(f"\n✅ Total Users: {len(users)}")
for user in users:
    print(f"   - ID: {user.user_id}, Name: {user.username}")

# Check LINE mappings
mappings = db.query(LineUserMapping).all()
print(f"\n✅ Total LINE Mappings: {len(mappings)}")
for mapping in mappings:
    print(f"   - LINE ID: {mapping.line_user_id}")
    print(f"     User ID: {mapping.user_id}")
    print(f"     Character ID: {mapping.character_id}")
    print(f"     Display Name: {mapping.line_display_name}")
    print()

db.close()

if len(chars) > 0 and len(mappings) == 0:
    print("⚠️  ISSUE FOUND: Characters exist but NO LINE mappings!")
    print("   This means the character was created but LINE integration failed.")
elif len(mappings) > 0:
    print("✅ LINE mappings exist - integration should work!")
