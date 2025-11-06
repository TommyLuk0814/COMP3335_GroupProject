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

def get_password_hash_by_id():
    # for login, check if the user is exist and return password hash
    conn = get_db_connection()
    sql = ""
    result = execute_query(conn, sql)
    
    conn.close()
    return result

def get_student_information_by_student_id():
    # student
    conn = get_db_connection()
    sql = ""
    result = execute_query(conn, sql)
    
    conn.close()
    return result

def update_student_information_sql():
    # student
    conn = get_db_connection()
    sql = ""
    result = execute_commit(conn, sql)
    
    conn.close()
    return result

def get_guardian_information_by_guardian_id():
    # student and guardain, when show student information or guardian information
    conn = get_db_connection()
    sql = ""
    result = execute_query(conn, sql)
    
    conn.close()
    return result

def update_guardian_information_sql():
    # guardian only
    conn = get_db_connection()
    sql = ""
    result = execute_commit(conn, sql)
    
    conn.close()
    return result

def list_all_grades_sql():
    # ARO only
    conn = get_db_connection()
    sql = ""
    result = execute_query(conn, sql)
    
    conn.close()
    return result

def list_grades_by_student_id():
    # ARO, student and guardian
    conn = get_db_connection()
    sql = ""
    result = execute_query(conn, sql)
    
    conn.close()
    return result

def list_grades_by_course_id():
    # ARO only
    conn = get_db_connection()
    sql = ""
    result = execute_query(conn, sql)
    
    conn.close()
    return result

def list_grades_by_term():
    # ARO only
    conn = get_db_connection()
    sql = ""
    result = execute_query(conn, sql)
    
    conn.close()
    return result

def add_grades_sql():
    # ARO only
    conn = get_db_connection()
    sql = ""
    result = execute_commit(conn, sql)
    
    conn.close()
    return result

def modify_grades_sql():
    # ARO only
    conn = get_db_connection()
    sql = ""
    result = execute_commit(conn, sql)
    
    conn.close()
    return result

def delete_grades_sql():
    # ARO only
    conn = get_db_connection()
    sql = ""
    result = execute_commit(conn, sql)
    
    conn.close()
    return result

def list_all_disciplinary_sql():
    # DRO only
    conn = get_db_connection()
    sql = ""
    result = execute_query(conn, sql)
    
    conn.close()
    return result

def list_disciplinary_by_student_id():
    # DRO, student and guardian
    conn = get_db_connection()
    sql = ""
    result = execute_query(conn, sql)
    
    conn.close()
    return result

def add_disciplinary_sql():
    # DRO only
    conn = get_db_connection()
    sql = ""
    result = execute_commit(conn, sql)
    
    conn.close()
    return result

def modify_disciplinary_sql():
    # DRO only
    conn = get_db_connection()
    sql = ""
    result = execute_commit(conn, sql)
    
    conn.close()
    return result

def delete_disciplinary_sql():
    # DRO only
    conn = get_db_connection()
    sql = ""
    result = execute_commit(conn, sql)
    
    conn.close()
    return result