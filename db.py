import mysql.connector

DB_CONFIG = {
    "host": "210.6.24.3",
    "user": "root",
    "password": "polyu",
    "database": "ComputingU",
    "port": 3306
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except mysql.connector.Error:
        return None #connection failed

