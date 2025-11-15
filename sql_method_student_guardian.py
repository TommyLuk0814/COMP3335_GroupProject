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
        'password': row[2],
        'first_name': row[3],
        'last_name': row[4]
    }

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
    sql = """
    SELECT id, last_name, first_name, gender, identification_number, 
           address, email, phone, enrollment_year
    FROM students 
    WHERE id = %s
    """

    result = execute_query(conn, sql, (student_id,))
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
    if not conn:
        return {'success': False, 'message': 'Failed to connect to database'}

    # Build dynamic query for allowed fields
    sql_parts = []
    params = []

    if 'address' in data and data['address'] is not None:
        sql_parts.append("address = %s")
        params.append(data['address'])

    if 'phone' in data and data['phone'] is not None:
        sql_parts.append("phone = %s")
        params.append(data['phone'])

    if 'email' in data and data['email'] is not None:
        sql_parts.append("email = %s")
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


# --- Replace the existing function in sql_method_student_guardian.py ---

def get_student_disciplinary_records_by_student_id(student_id):
    # Fetches all disciplinary records for a specific student, joining staff name
    conn = get_db_connection()
    sql = """
    SELECT dr.id, dr.date, dr.descriptions, 
           s.first_name as staff_first, s.last_name as staff_last
    FROM disciplinary_records dr
    JOIN staffs s ON dr.staff_id = s.id
    WHERE dr.student_id = %s
    ORDER BY dr.date DESC
    """
    result = execute_query(conn, sql, (student_id,))

    conn.close()
    return result

# --------------------------------------------------------------------