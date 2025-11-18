from db import get_db_connection
from encryption import get_aes_key  # Added: Import the key function


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
        raise e  # Modified: Propagate the error


def get_staff_information_by_email(email):
    conn = get_db_connection()
    sql = "SELECT id, email, password, first_name, last_name, role FROM staffs WHERE email = %s"
    result = execute_query(conn, sql, (email,))

    conn.close()
    if result and len(result) > 0:
        row = result[0]
        return {
            'id': row[0],
            'email': row[1],
            'password': row[2],
            'first_name': row[3],
            'last_name': row[4],
            'role': row[5]  # 'ARO', 'DRO'
        }
    # Added: Ensure None is returned if no user is found
    return None


# maybe dont need that
# def get_aro_information_by_email(email):
#     conn = get_db_connection()
#     sql = "SELECT * FROM staffs WHERE email = %s AND role = 'ARO'"
#     result = execute_query(conn, sql, email)
#
#     conn.close()
#     return result
#
# def get_dro_information_by_email(email):
#     conn = get_db_connection()
#     sql = "SELECT * FROM staffs WHERE email = %s AND role = 'DRO'"
#     result = execute_query(conn, sql, email)
#
#     conn.close()
#     return result

def list_all_grades_sql():
    conn = get_db_connection()
    sql = """
    SELECT g.id, g.student_id, s.first_name, s.last_name, 
           g.course_id, c.course_name, g.term, g.grade, g.comments
    FROM grades g
    JOIN students s ON g.student_id = s.id
    JOIN courses c ON g.course_id = c.id
    ORDER BY g.term DESC, s.last_name, s.first_name
    """
    result = execute_query(conn, sql)

    conn.close()
    return result


def list_grades_by_student_id(student_id):
    conn = get_db_connection()
    sql = """
    SELECT g.id, g.student_id, s.first_name, s.last_name, 
           g.course_id, c.course_name, g.term, g.grade, g.comments
    FROM grades g
    JOIN students s ON g.student_id = s.id
    JOIN courses c ON g.course_id = c.id
    WHERE g.student_id = %s
    ORDER BY g.term DESC
    """
    result = execute_query(conn, sql, (student_id,))

    conn.close()
    return result


def check_grade_exists(student_id, course_id, term):
    conn = get_db_connection()
    sql = """
    SELECT id FROM grades 
    WHERE student_id = %s AND course_id = %s AND term = %s
    """
    result = execute_query(conn, sql, (student_id, course_id, term))

    conn.close()
    return result[0][0] if result and len(result) > 0 else None


def check_disciplinary_exists(student_id, date):
    conn = get_db_connection()
    sql = """
    SELECT id FROM disciplinary_records 
    WHERE student_id = %s AND date = %s
    """
    result = execute_query(conn, sql, (student_id, date))

    conn.close()
    return result[0][0] if result and len(result) > 0 else None


def add_grades_sql(student_id, course_id, term, grade, comments=""):
    conn = get_db_connection()
    if not conn:
        return False

    try:
        # 1. check if exist
        check_sql = """
        SELECT id FROM grades 
        WHERE student_id = %s AND course_id = %s AND term = %s
        """
        with conn.cursor() as cursor:
            cursor.execute(check_sql, (student_id, course_id, term))
            existing_record = cursor.fetchone()

            if existing_record:
                return False

                # 2. not exist,do:
        insert_sql = """
        INSERT INTO grades (student_id, course_id, term, grade, comments)
        VALUES (%s, %s, %s, %s, %s)
        """
        execute_commit(conn, insert_sql, (student_id, course_id, term, grade, comments))
        # Modified: Return True on success
        return True

    except Exception as e:
        return False
    finally:
        if conn:
            conn.close()


def modify_grades_sql(grade_id, grade, comments):
    conn = get_db_connection()
    sql = """
    UPDATE grades 
    SET grade = %s, comments = %s 
    WHERE id = %s
    """
    try:
        execute_commit(conn, sql, (grade, comments, grade_id))
        # Modified: Return True on success
        return True
    except Exception as e:
        return False
    finally:
        if conn:
            conn.close()


def delete_grades_sql(grades_id):
    conn = get_db_connection()
    sql = "DELETE FROM grades WHERE id = %s"
    try:
        execute_commit(conn, sql, (grades_id,))
        # Modified: Return True on success
        return True
    except Exception as e:
        return False
    finally:
        if conn:
            conn.close()


def list_all_disciplinary_sql():
    conn = get_db_connection()
    key = get_aes_key()  # Added: Get AES key

    # Modified: Use AES_DECRYPT for descriptions
    sql = """
    SELECT d.id, d.student_id, s.first_name, s.last_name, 
           d.date, st.first_name as staff_first_name, st.last_name as staff_last_name,
           CAST(AES_DECRYPT(d.descriptions, %s) AS CHAR) as descriptions
    FROM disciplinary_records d
    JOIN students s ON d.student_id = s.id
    JOIN staffs st ON d.staff_id = st.id
    ORDER BY d.date DESC
    """
    # Modified: Pass key to query
    result = execute_query(conn, sql, (key,))

    conn.close()
    return result


def list_disciplinary_by_student_id(student_id):
    conn = get_db_connection()
    key = get_aes_key()  # Added: Get AES key

    # Modified: Use AES_DECRYPT for descriptions
    sql = """
    SELECT d.id, d.student_id, s.first_name, s.last_name, 
           d.date, st.first_name as staff_first_name, st.last_name as staff_last_name,
           CAST(AES_DECRYPT(d.descriptions, %s) AS CHAR) as descriptions
    FROM disciplinary_records d
    JOIN students s ON d.student_id = s.id
    JOIN staffs st ON d.staff_id = st.id
    WHERE d.student_id = %s
    ORDER BY d.date DESC
    """
    # Modified: Pass key and student_id
    result = execute_query(conn, sql, (key, student_id))

    conn.close()
    return result


def add_disciplinary_sql(student_id, staff_id, date, descriptions):
    conn = get_db_connection()
    key = get_aes_key()  # Added: Get AES key

    # Modified: Use AES_ENCRYPT for descriptions
    sql = """
    INSERT INTO disciplinary_records (student_id, staff_id, date, descriptions)
    VALUES (%s, %s, %s, AES_ENCRYPT(%s, %s))
    """
    try:
        # Modified: Pass descriptions and key
        execute_commit(conn, sql, (student_id, staff_id, date, descriptions, key))
        return True
    except Exception as e:
        return False
    finally:
        if conn:
            conn.close()


def modify_disciplinary_sql(disciplinary_id, descriptions, staff_id):
    conn = get_db_connection()
    key = get_aes_key()  # Added: Get AES key

    # Modified: Use AES_ENCRYPT for descriptions
    sql = """
    UPDATE disciplinary_records 
    SET descriptions = AES_ENCRYPT(%s, %s), staff_id = %s
    WHERE id = %s
    """
    try:
        # Modified: Pass descriptions, key, staff_id, and disciplinary_id
        execute_commit(conn, sql, (descriptions, key, staff_id, disciplinary_id))
        return True
    except Exception as e:
        return False
    finally:
        if conn:
            conn.close()


def delete_disciplinary_sql(disciplinary_id):
    conn = get_db_connection()
    sql = "DELETE FROM disciplinary_records WHERE id = %s"
    try:
        execute_commit(conn, sql, (disciplinary_id,))
        # Modified: Return True on success
        return True
    except Exception as e:
        return False
    finally:
        if conn:
            conn.close()


def list_student_sql():
    conn = get_db_connection()
    sql = "SELECT id, first_name, last_name FROM students ORDER BY last_name, first_name"
    result = execute_query(conn, sql)

    conn.close()
    return result


def list_course_sql():
    conn = get_db_connection()
    sql = "SELECT id, course_name FROM courses ORDER BY course_name"
    result = execute_query(conn, sql)

    conn.close()
    return result


def list_staff_sql():
    conn = get_db_connection()
    sql = "SELECT id, first_name, last_name FROM staffs ORDER BY last_name, first_name"
    result = execute_query(conn, sql)

    conn.close()
    return result