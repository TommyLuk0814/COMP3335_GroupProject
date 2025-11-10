from db import get_db_connection

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

if __name__ == "__main__":
    main()