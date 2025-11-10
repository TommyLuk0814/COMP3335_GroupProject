from db import get_db_connection

def execute_query(conn, sql, params=None):
    # for select sql
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
    except Exception as e:
        print(f"Query error: {e}")
        return None

def execute_commit(conn, query, params=None):
    # for insert, update and delete sql
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()
    except Exception as e:
        print(f"Insert error: {e}")
        conn.rollback()


def get_student_information_by_email(email):
    conn = get_db_connection()
    sql = "SELECT id, email, password, first_name, last_name FROM students WHERE email = %s"
    result = execute_query(conn, sql, (email,))

    conn.close()
    if result and len(result) > 0:
        row = result[0]
        return {
            'id': row[0],
            'email': row[1],
            'password_hash': row[2],
            'first_name': row[3],
            'last_name': row[4]
        }
    return None


def get_guardian_information_by_email(email):
    conn = get_db_connection()
    sql = "SELECT id, email, password, first_name, last_name FROM guardians WHERE email = %s"
    result = execute_query(conn, sql, (email,))

    conn.close()
    if result and len(result) > 0:
        row = result[0]
        return {
            'id': row[0],
            'email': row[1],
            'password_hash': row[2],
            'first_name': row[3],
            'last_name': row[4]
        }
    return None


def get_student_information_by_student_id(student_id):
    conn = get_db_connection()
    sql = ""
    result = execute_query(conn, sql, student_id)
    
    conn.close()
    return result

def get_student_information_by_guardian_id(guardian_id):
    conn = get_db_connection()
    sql = ""
    result = execute_query(conn, sql, guardian_id)
    
    conn.close()
    return result

def update_student_information_sql():
    conn = get_db_connection()
    sql = ""
    result = execute_commit(conn, sql)
    
    conn.close()
    return result

def get_guardian_information_by_guardian_id(guardian_id):
    conn = get_db_connection()
    sql = ""
    result = execute_query(conn, sql, guardian_id)
    
    conn.close()
    return result

def update_guardian_information_sql():
    conn = get_db_connection()
    sql = ""
    result = execute_commit(conn, sql)
    
    conn.close()
    return result