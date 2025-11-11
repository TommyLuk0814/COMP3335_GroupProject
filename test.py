from db import get_db_connection
from werkzeug.security import generate_password_hash

def main():
    test_password = "password123"
    hashed = generate_password_hash(test_password)

    conn = get_db_connection()
    if not conn:
        print("fail to connect db")
        return

    cursor = conn.cursor()

    cursor.execute("UPDATE students SET password = %s", (hashed,))
    cursor.execute("UPDATE guardians SET password = %s", (hashed,))
    cursor.execute("UPDATE staffs SET password = %s", (hashed,))

    conn.commit()
    conn.close()

    print(f"測試密碼：{test_password}")
    print(f"Hash：{hashed}")

if __name__ == "__main__":
    main()
