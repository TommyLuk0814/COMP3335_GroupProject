import os

from flask import Flask, request, jsonify, send_from_directory, render_template
from controller import *
from sql_method_student_guardian import *
from sql_method_ARO_DRO import *
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity,
    JWTManager, get_jwt, set_access_cookies, unset_jwt_cookies
)
from werkzeug.security import check_password_hash, generate_password_hash

from functools import wraps


app = Flask(__name__, template_folder='front/templates')

app.config['JWT_SECRET_KEY'] = 'helloxixixixixixixixixixixixi'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600 #token expires in 1 hour
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
jwt = JWTManager(app)



@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    # When the token expires, redirect to the error page.
    return render_template('error.html', message="Session expired. Please log in again."), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    # When there is no token in the request (e.g., not logged in)
    return render_template('error.html', message="Access Denied. You are not logged in."), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    # When the token is invalid (e.g., format error)
    return render_template('error.html', message="Invalid session token. Please log in again."), 422


def roles_required(required_roles):

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Ensure that the JWT exists first.
            claims = get_jwt()
            user_role = claims.get('role')

            if user_role not in required_roles:
                return jsonify({'message': f'Access denied: Role "{user_role}" is not authorized.'}), 403

            # If the role is a match, then execute the original routing function.
            return fn(*args, **kwargs)

        return wrapper

    return decorator

@app.route("/")
def serve_login_page():
    """
    when the user visits the website root directory (http://127.0.0.1:5000/),
    display the login page.
    """
    # this will look for 'login.html' in the 'front/templates/' folder.
    return render_template('login.html')


#dont set jwt require
#as users token may expire when accessing the page
#so need to catch the error and jump to error website
@app.route('/<role_folder>/<page_name>')
@jwt_required()
def serve_protected_page(role_folder, page_name):
    try:
        claims = get_jwt()
        user_role = claims.get('role')

        # make a mapping between roles and folder names
        role_to_folder_map = {
            'student': 'student',
            'guardian': 'Guardian',
            'ARO': 'ARO',
            'DRO': 'DRO'
        }

        # Check if the logged-in user's role corresponds to the folder they want to access.
        if role_to_folder_map.get(user_role) == role_folder:
            # correct role
            path = os.path.join(role_folder, page_name)
            return render_template(path)
        else:
            return render_template('error.html', message="Access Denied. Invalid role."), 403

    except Exception as e:
        print(e)
        return render_template('error.html', message="Page not found or session expired."), 404

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')  # 'student', 'guardian', 'staff'

    if role not in ['student', 'guardian', 'staff']:
        return jsonify({'message': 'Invalid role'}), 400

    # check the password from dirrerent tables
    if role == 'student':
        user_info = get_student_information_by_email(email)
    elif role == 'guardian':
        user_info = get_guardian_information_by_email(email)
    else:  # staff
        user_info = get_staff_information_by_email(email)

    #print(user_info.get("first_name"), user_info.get("last_name"))
    if not user_info:
        return jsonify({'message': 'Invalid credentials'}), 401

    # compare password hash
    if not check_password_hash(user_info.get('password'), password):
        return jsonify({'message': 'Invalid credentials'}), 401

    actual_role = role
    if role == 'staff':
        actual_role = user_info.get('role')  # 'ARO', 'DRO'

    # create jwt token
    user_id = user_info.get('id')
    additional_claims = {
        'role': actual_role,
        'user_id': user_id
    }
    access_token = create_access_token(identity=email, additional_claims=additional_claims)

    response_data = {
        'access_token': access_token,
        'role': actual_role,
        'user_id': user_id,
        'name': f"{user_info.get('first_name')} {user_info.get('last_name')}"
    }


    resp = jsonify(response_data)


    set_access_cookies(resp, access_token)

    return resp, 200

@app.route("/logout", methods=["POST"])
def logout():
    resp = jsonify({'message': 'Logout successful'})
    # clear jwt cookei
    unset_jwt_cookies(resp)
    return resp, 200



@app.route("/check_information", methods=["GET"])
@jwt_required()
def check_information():
    current_user = get_jwt_identity()
    claims = get_jwt()
    role = claims.get('role')
    user_id = claims.get('user_id')

    if role not in ['student', 'guardian']:
        return jsonify({'message': 'Access denied'}), 403

    result = check_information_controller(user_id)
    return result



@app.route("/maintain_information", methods=["PUT"])
def maintain_information():
    # student and guardian
    data = request
    
    result = maintain_information_controller(data)
    
    return result

@app.route("/check_grades", methods=["GET"])
def check_grades():
    # student, guardian
    
    result = list_grades_by_student_id()
    
    return result

@app.route("/check_disciplinary", methods=["GET"])
def check_disciplinary():
    # student, guardian
    
    result = list_disciplinary_by_student_id()
    
    return result

@app.route("/list_grades", methods=["GET"])
@jwt_required()
@roles_required(['ARO'])
def list_grades():
    # ARO Only
    
    student_id = request.args.get('student_id')
    
    if student_id:
        result = list_grades_by_student_id(student_id)
    else:
        result = list_all_grades_sql()
    
    return jsonify(result) if result else jsonify([])
    

@app.route("/add_grades", methods=["POST"])
@jwt_required()
@roles_required(['ARO'])
def add_grades():
    # ARO Only
    
    data = request.get_json()
    
    student_id = data.get('student_id')
    course_id = data.get('course_id')
    term = data.get('term')
    grade = data.get('grade')
    comments = data.get('comments', '')

    existing_grade_id = check_grade_exists(student_id, course_id, term)
    if existing_grade_id:
        # if the grade record exists, modify it instead
        result = modify_grades_sql(existing_grade_id, grade, comments)
        return jsonify({'success': result, 'action': 'modified'})
    else:
        result = add_grades_sql(student_id, course_id, term, grade, comments)
        return jsonify({'success': result, 'action': 'added'})
    

@app.route("/modify_grades", methods=["PUT"])
@jwt_required()
@roles_required(['ARO'])
def modify_grades():
    # ARO Only
    
    data = request.get_json()
    
    grade_id = data.get('grade_id')
    grade = data.get('grade')
    comments = data.get('comments', '')
    
    result = modify_grades_sql(grade_id, grade, comments)
    
    return jsonify({'success': result})
    

@app.route("/delete_grades", methods=["DELETE"])
@jwt_required()
@roles_required(['ARO'])
def delete_grades():
    # ARO Only
    
    grades_id = request.args.get('grades_id')
    
    result = delete_grades_sql(grades_id)
    
    return jsonify({'success': result})
    

@app.route("/list_disciplinary", methods=["GET"])
@jwt_required()
@roles_required(['DRO'])
def list_disciplinary():
    # DRO Only
    
    student_id = request.args.get('student_id')
    
    if student_id:
        result = list_disciplinary_by_student_id(student_id)
    else:
        result = list_all_disciplinary_sql()
    
    return jsonify(result) if result else jsonify([])

@app.route("/add_disciplinary", methods=["POST"])
@jwt_required()
@roles_required(['DRO'])
def add_disciplinary():
    # DRO Only
    
    data = request.get_json()
    
    student_id = data.get('student_id')
    staff_id = data.get('staff_id')
    date = data.get('date')
    descriptions = data.get('descriptions')


    existing_record_id = check_disciplinary_exists(student_id, date)
    if existing_record_id:
        # if the grade record exists, modify it instead
        result = modify_disciplinary_sql(existing_record_id, descriptions,staff_id)
        return jsonify({'success': result, 'action': 'modified'})
    else:
        result = add_disciplinary_sql(student_id, staff_id, date, descriptions)
        return jsonify({'success': result, 'action': 'added'})


@app.route("/modify_disciplinary", methods=["PUT"])
@jwt_required()
@roles_required(['DRO'])
def modify_disciplinary():
    # DRO Only
    
    data = request.get_json()
    
    disciplinary_id = data.get('disciplinary_id')
    descriptions = data.get('descriptions')
    staff_id = data.get('staff_id')
    
    result = modify_disciplinary_sql(disciplinary_id, descriptions,staff_id)
    
    return jsonify({'success': result})

@app.route("/delete_disciplinary", methods=["DELETE"])
@jwt_required()
@roles_required(['DRO'])
def delete_disciplinary():
    # DRO Only
    
    disciplinary_id = request.args.get('disciplinary_id')
    
    result = delete_disciplinary_sql(disciplinary_id)
    return jsonify({'success': result})

@app.route("/guardian_children", methods=["GET"])
@jwt_required()
@roles_required(['guardian'])
def guardian_children():
    claims = get_jwt()
    guardian_id = claims.get('user_id')

    result = get_student_information_by_guardian_id(guardian_id)

    return jsonify(result) if result else jsonify([])


@app.route("/list_student", methods=["GET"])
@jwt_required()
def list_student():
    # ARO and DRO
    
    result = list_student_sql()
    return jsonify(result) if result else jsonify([])

@app.route("/list_course", methods=["GET"])
@jwt_required()
def list_course():
    # ARO only
    
    result = list_course_sql()
    return jsonify(result) if result else jsonify([])

@app.route("/list_staff", methods=["GET"])
def list_staff():
    # DRO only
    
    result = list_staff_sql()
    return jsonify(result) if result else jsonify([])



@app.route("/student/my_grades", methods=["GET"])
@jwt_required()
@roles_required(['student'])
def get_my_grades():
    # Get student ID from token
    claims = get_jwt()
    student_id = claims.get('user_id')

    if not student_id:
        return jsonify({'message': 'User ID not found in token'}), 400

    # Call function from sql_method_student_guardian
    result = get_student_grades_by_student_id(student_id)

    return jsonify(result) if result else jsonify([])


@app.route("/student/my_profile", methods=["GET"])
@jwt_required()
@roles_required(['student'])
def get_my_profile():
    claims = get_jwt()
    student_id = claims.get('user_id')

    if not student_id:
        return jsonify({'message': 'User ID not found in token'}), 400

    # Call function from sql_method_student_guardian
    profile_data = get_student_profile_by_id(student_id)

    if not profile_data:
        return jsonify({'message': 'Student profile not found'}), 404

    return jsonify(profile_data)


@app.route("/student/my_profile", methods=["PUT"])
@jwt_required()
@roles_required(['student'])
def update_my_profile():
    claims = get_jwt()
    student_id = claims.get('user_id')

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    # Call function from sql_method_student_guardian
    result = update_student_profile(student_id, data)

    if result['success']:
        return jsonify({'message': result['message']}), 200
    else:
        # Distinguish between conflict (duplicate email) and other errors
        if 'already in use' in result['message']:
            return jsonify({'message': result['message']}), 409  # 409 Conflict
        else:
            return jsonify({'message': result['message']}), 500  # 500 Internal Server Error



@app.route("/student/my_disciplinary", methods=["GET"])
@jwt_required()
@roles_required(['student'])
def get_my_disciplinary_records():
    # Get student ID from token
    claims = get_jwt()
    student_id = claims.get('user_id')

    if not student_id:
        return jsonify({'message': 'User ID not found in token'}), 400

    # Call the corrected function from sql_method_student_guardian
    result = get_student_disciplinary_records_by_student_id(student_id)

    return jsonify(result) if result else jsonify([])


# --- Please add these two routes to server.py ---

@app.route("/guardian/my_profile", methods=["GET"])
@jwt_required()
@roles_required(['guardian'])
def get_guardian_profile():
    claims = get_jwt()
    guardian_id = claims.get('user_id')

    if not guardian_id:
        return jsonify({'message': 'User ID not found in token'}), 400

    profile_data = get_guardian_profile_by_id(guardian_id)

    if not profile_data:
        return jsonify({'message': 'Guardian profile not found'}), 404

    return jsonify(profile_data)


@app.route("/guardian/my_profile", methods=["PUT"])
@jwt_required()
@roles_required(['guardian'])
def handle_update_guardian_profile():
    claims = get_jwt()
    guardian_id = claims.get('user_id')

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    result = update_guardian_profile(guardian_id, data)

    if result['success']:
        return jsonify({'message': result['message']}), 200
    else:
        if 'already in use' in result['message']:
            return jsonify({'message': result['message']}), 409  # Conflict
        else:
            return jsonify({'message': result['message']}), 500  # Server Error





if __name__ == "__main__":
    app.run(debug=True, port=5000)
