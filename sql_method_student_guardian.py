from db import get_db_connection
from encryption import get_aes_key
import logging

def execute_query(conn, sql, params=None):
    # for select sql
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
    except Exception as e:
        # --- Modified: Replaced print with logging.error ---
        # This will log any database query error, which could indicate
        # a failed SQL injection attempt or other DB problem.
        # exc_info=True logs the full error stack trace.
        logging.error(
            f"[DB ERROR - QUERY] Failed to execute query. SQL: {sql}, Params: {params}, Error: {e}",
            exc_info=True
        )
        # --- End Modification ---
        return None


def execute_commit(conn, query, params=None):
    # for insert, update and delete sql
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()
    except Exception as e:
        # --- Modified: Replaced print with logging.error ---
        # This logs any database commit error (INSERT, UPDATE, DELETE).
        logging.error(
            f"[DB ERROR - COMMIT] Failed to execute commit. SQL: {query}, Params: {params}, Error: {e}",
            exc_info=True
        )
        conn.rollback()
        raise e

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
            'password': row[2],
            'first_name': row[3],
            'last_name': row[4]
        }
    # Added: Ensure None is returned if no user is found
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
            'password': row[2],
            'first_name': row[3],
            'last_name': row[4]
        }
    # Added: Ensure None is returned if no user is found
    return None


def get_student_information_by_guardian_id(guardian_id):
    conn = get_db_connection()
    sql = "SELECT id, first_name, last_name, guardian_relation FROM students WHERE guardian_id = %s"

    result = execute_query(conn, sql, (guardian_id,))

    conn.close()
    return result


def get_student_grades_by_student_id(student_id):
    # Fetches all grades for a specific student, joining course name
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
    # Pass student_id as a tuple
    result = execute_query(conn, sql, (student_id,))

    conn.close()
    return result


def get_student_profile_by_id(student_id):
    # Fetches non-sensitive profile data for a student
    conn = get_db_connection()
    key = get_aes_key()  # Added: Get AES key

    # Modified: Use AES_DECRYPT for encrypted fields
    sql = """
    SELECT id, last_name, first_name, gender, 
           CAST(AES_DECRYPT(identification_number, %s) AS CHAR) as identification_number, 
           CAST(AES_DECRYPT(address, %s) AS CHAR) as address, 
           email, 
           CAST(AES_DECRYPT(phone, %s) AS CHAR) as phone, 
           enrollment_year
    FROM students 
    WHERE id = %s
    """

    # Modified: Pass the key for each decrypted field, plus the student_id
    result = execute_query(conn, sql, (key, key, key, student_id))
    conn.close()

    if result and len(result) > 0:
        row = result[0]
        # Convert tuple to dictionary for easier JSON handling
        profile_data = {
            'id': row[0],
            'last_name': row[1],
            'first_name': row[2],
            'gender': row[3],
            'identification_number': row[4],
            'address': row[5],
            'email': row[6],
            'phone': row[7],
            'enrollment_year': row[8]
        }
        return profile_data

    return None


def update_student_profile(student_id, data):
    # Updates student profile with data from the form
    conn = get_db_connection()
    key = get_aes_key()  # Added: Get AES key

    if not conn:
        return {'success': False, 'message': 'Failed to connect to database'}

    # Build dynamic query for allowed fields
    sql_parts = []
    params = []

    if 'address' in data and data['address'] is not None:
        # Modified: Use AES_ENCRYPT for address
        sql_parts.append("address = AES_ENCRYPT(%s, %s)")
        params.append(data['address'])
        params.append(key)  # Added: Pass key

    if 'phone' in data and data['phone'] is not None:
        # Modified: Use AES_ENCRYPT for phone
        sql_parts.append("phone = AES_ENCRYPT(%s, %s)")
        params.append(data['phone'])
        params.append(key)  # Added: Pass key

    if 'email' in data and data['email'] is not None:
        sql_parts.append("email = %s")  # No encryption for email
        params.append(data['email'])

    if not sql_parts:
        conn.close()
        return {'success': False, 'message': 'No valid fields to update'}

    params.append(student_id)
    sql = f"UPDATE students SET {', '.join(sql_parts)} WHERE id = %s"

    try:
        execute_commit(conn, sql, tuple(params))
        conn.close()
        return {'success': True, 'message': 'Profile updated successfully'}
    except Exception as e:
        conn.rollback()
        conn.close()
        # Handle unique constraint violation for email
        if 'email' in str(e) and 'Duplicate entry' in str(e):
            return {'success': False, 'message': 'Update failed: This email address is already in use.'}
        return {'success': False, 'message': f'Update failed: {str(e)}'}


def get_student_disciplinary_records_by_student_id(student_id):
    # Fetches all disciplinary records for a specific student, joining staff name
    conn = get_db_connection()
    key = get_aes_key()  # Added: Get AES key

    # Modified: Use AES_DECRYPT for descriptions
    sql = """
    SELECT dr.id, dr.date, 
           CAST(AES_DECRYPT(dr.descriptions, %s) AS CHAR) as descriptions, 
           s.first_name as staff_first, s.last_name as staff_last
    FROM disciplinary_records dr
    JOIN staffs s ON dr.staff_id = s.id
    WHERE dr.student_id = %s
    ORDER BY dr.date DESC
    """
    # Modified: Pass key and student_id
    result = execute_query(conn, sql, (key, student_id))

    conn.close()
    return result


def get_guardian_profile_by_id(guardian_id):
    # Fetches non-sensitive profile data for a guardian
    conn = get_db_connection()
    key = get_aes_key()  # Added: Get AES key

    # Based on database.sql, guardians table has fewer personal columns
    # Modified: Use AES_DECRYPT for phone
    sql = """
    SELECT id, last_name, first_name, email, 
           CAST(AES_DECRYPT(phone, %s) AS CHAR) as phone
    FROM guardians 
    WHERE id = %s
    """

    # Modified: Pass key and guardian_id
    result = execute_query(conn, sql, (key, guardian_id))
    conn.close()

    if result and len(result) > 0:
        row = result[0]
        # Convert tuple to dictionary
        profile_data = {
            'id': row[0],
            'last_name': row[1],
            'first_name': row[2],
            'email': row[3],
            'phone': row[4]
        }
        return profile_data

    return None


def update_guardian_profile(guardian_id, data):
    # Updates guardian profile with data from the form
    conn = get_db_connection()
    key = get_aes_key()  # Added: Get AES key

    if not conn:
        return {'success': False, 'message': 'Failed to connect to database'}

    sql_parts = []
    params = []

    # Guardians can only update email and phone
    if 'email' in data and data['email'] is not None:
        sql_parts.append("email = %s")  # No encryption for email
        params.append(data['email'])

    if 'phone' in data and data['phone'] is not None:
        # Modified: Use AES_ENCRYPT for phone
        sql_parts.append("phone = AES_ENCRYPT(%s, %s)")
        params.append(data['phone'])
        params.append(key)  # Added: Pass key

    if not sql_parts:
        conn.close()
        return {'success': False, 'message': 'No valid fields to update'}

    params.append(guardian_id)
    sql = f"UPDATE guardians SET {', '.join(sql_parts)} WHERE id = %s"

    try:
        execute_commit(conn, sql, tuple(params))
        conn.close()
        return {'success': True, 'message': 'Profile updated successfully'}
    except Exception as e:
        # If we are here, execute_commit failed (e.g., duplicate email)
        conn.close()
        if 'email' in str(e) and 'Duplicate entry' in str(e):
            return {'success': False, 'message': 'Update failed: This email address is already in use.'}
        # Return a generic error for other SQL problems
        return {'success': False, 'message': f'Update failed: {str(e)}'}


def is_guardian_of_student(guardian_id, student_id):
    """
    Checks if a given guardian_id is the guardian of a given student_id.
    Returns True if they are, False otherwise.
    """
    conn = get_db_connection()
    if not conn:
        print("Database connection failed in is_guardian_of_student")
        return False

    sql = "SELECT id FROM students WHERE id = %s AND guardian_id = %s"

    result = None
    try:
        # Pass params as a tuple
        result = execute_query(conn, sql, (student_id, guardian_id))
    except Exception as e:
        print(f"Error checking guardian relationship: {e}")
        return False  # Fail safe
    finally:
        if conn:
            conn.close()

    # If a record is found (result is not None and has length > 0), return True
    return result and len(result) > 0