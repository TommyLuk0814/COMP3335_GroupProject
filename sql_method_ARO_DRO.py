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

def get_aro_information_by_email(email):
    conn = get_db_connection()
    sql = ""
    result = execute_query(conn, sql, email)
    
    conn.close()
    return result

def get_dro_information_by_email(email):
    conn = get_db_connection()
    sql = ""
    result = execute_query(conn, sql, email)
    
    conn.close()
    return result
        
def list_all_grades_sql():
    conn = get_db_connection()
    sql = ""
    result = execute_query(conn, sql)
    
    conn.close()
    return result

def list_grades_by_student_id(student_id):
    conn = get_db_connection()
    sql = ""
    result = execute_query(conn, sql, student_id)
    
    conn.close()
    return result

def add_grades_sql():
    conn = get_db_connection()
    sql = ""
    result = execute_commit(conn, sql)
    
    conn.close()
    return result

def modify_grades_sql():
    conn = get_db_connection()
    sql = ""
    result = execute_commit(conn, sql)
    
    conn.close()
    return result

def delete_grades_sql(grades_id):
    conn = get_db_connection()
    sql = ""
    result = execute_commit(conn, sql, grades_id)
    
    conn.close()
    return result

def list_all_disciplinary_sql():
    conn = get_db_connection()
    sql = ""
    result = execute_query(conn, sql)
    
    conn.close()
    return result

def list_disciplinary_by_student_id(student_id):
    conn = get_db_connection()
    sql = ""
    result = execute_query(conn, sql, student_id)
    
    conn.close()
    return result

def add_disciplinary_sql():
    conn = get_db_connection()
    sql = ""
    result = execute_commit(conn, sql)
    
    conn.close()
    return result

def modify_disciplinary_sql():
    conn = get_db_connection()
    sql = ""
    result = execute_commit(conn, sql)
    
    conn.close()
    return result

def delete_disciplinary_sql(disciplinary_id):
    conn = get_db_connection()
    sql = ""
    result = execute_commit(conn, sql, disciplinary_id)
    
    conn.close()
    return result

def list_student_sql():
    conn = get_db_connection()
    sql = ""
    result = execute_query(conn, sql)
    
    conn.close()
    return result

def list_course_sql():
    conn = get_db_connection()
    sql = ""
    result = execute_query(conn, sql)
    
    conn.close()
    return result

def list_staff_sql():
    conn = get_db_connection()
    sql = ""
    result = execute_query(conn, sql)
    
    conn.close()
    return result