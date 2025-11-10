from db import get_db_connection

import hashlib
import secrets
import string

def main():
    conn = get_db_connection()
    if not conn:
        print("Connection failed")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print("Connected. SELECT 1 ->", result)
    except Exception as e:
        print("Query failed:", e)
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        conn.close()

def generate_random_password(length=12):
    "Generate a random password"
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Generate three random passwords.
for i in range(1, 4):
    password = generate_random_password()
    hashed = hash_password(password)
    print(f"user {i}:")
    print(f"  origin pw: {password}")
    print(f"  hash pw: {hashed}")
    print()


if __name__ == "__main__":
    main()