import mysql.connector
from db import get_db_connection

def execute_query(conn, query, params=None):
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    except Exception as e:
        print(f"SQL Query error: {e}")
        return None

def login_sql(email, password):
    conn = get_db_connection()
    #check if the user if exist
    return None