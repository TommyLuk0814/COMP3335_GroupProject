import os

from flask import Flask, request, jsonify, send_from_directory, render_template
from controller import *
from sql_method_student_guardian import *
from sql_method_ARO_DRO import *
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager, get_jwt
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__, template_folder='front/templates')

app.config['JWT_SECRET_KEY'] = 'helloxixixixixixixixixixixixi'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # Token exp in 1 hour

jwt = JWTManager(app)


@app.route("/")
def serve_login_page():
    """
    when the user visits the website root directory (http://127.0.0.1:5000/),
    display the login page.
    """
    # this will look for 'login.html' in the 'front/templates/' folder.
    return render_template('login.html')


@app.route('/<role_folder>/<page_name>')
@jwt_required()
def serve_protected_page(role_folder, page_name):
    """
    Dynamic routing:
    - /student/profile.html
    - /ARO/manage_grades.html
    - /DRO/manage_disciplinary.html
    """
    try:
        claims = get_jwt()
        user_role = claims.get('role')

        #only the matching role can access their pages
        if (user_role == 'student' and role_folder == 'student') or \
                (user_role == 'guardian' and role_folder == 'Guardian') or \
                (user_role == 'ARO' and role_folder == 'ARO') or \
                (user_role == 'DRO' and role_folder == 'DRO'):

            # conbinate role_folder and page_name to form the path
            # e.g., 'student/profile.html'
            path = os.path.join(role_folder, page_name)

            return render_template(path)
        else:
            # if the role aceess a page not belong to them
            # say goodbye
            return render_template('error.html', message="Access Denied"), 403

    except Exception as e:
        print(e)
        return render_template('error.html', message="Page not found or error"), 404


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
        user_info = get_student_by_email(email)
    elif role == 'guardian':
        user_info = get_guardian_by_email(email)
    else:  # staff
        user_info = get_staff_by_email(email)

    if not user_info:
        return jsonify({'message': 'Invalid credentials'}), 401

    # compare password hash
    if not check_password_hash(user_info.get('password_hash'), password):
        return jsonify({'message': 'Invalid credentials'}), 401

    # create jwt token
    user_id = user_info.get('id')
    additional_claims = {
        'role': role,
        'user_id': user_id
    }
    access_token = create_access_token(identity=email, additional_claims=additional_claims)

    return jsonify({
        'access_token': access_token,
        'role': role,
        'user_id': user_id
    }), 200


@app.route("/check_information", methods=["GET"])
@jwt_required()
def check_information():
    current_user = get_jwt_identity()
    claims = get_jwt()
    role = claims.get('role')
    user_id = claims.get('user_id')

    # 只允許 student 和 guardian
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
def list_grades():
    # ARO Only
    
    student_id = request.args.get('student_id')
    
    if student_id:
        result = list_grades_by_student_id(student_id)
    else:
        result = list_all_grades_sql()
    
    return jsonify(result) if result else jsonify([])
    

@app.route("/add_grades", methods=["POST"])
def add_grades():
    # ARO Only
    
    data = request.get_json()
    
    student_id = data.get('student_id')
    course_id = data.get('course_id')
    term = data.get('term')
    grade = data.get('grade')
    comments = data.get('comments', '')
    
    result = add_grades_sql(student_id, course_id, term, grade, comments)
    
    return jsonify({'success': result})
    

@app.route("/modify_grades", methods=["PUT"])
def modify_grades():
    # ARO Only
    
    data = request.get_json()
    
    grade_id = data.get('grade_id')
    grade = data.get('grade')
    comments = data.get('comments', '')
    
    result = modify_grades_sql(grade_id, grade, comments)
    
    return jsonify({'success': result})
    

@app.route("/delete_grades", methods=["DELETE"])
def delete_grades():
    # ARO Only
    
    grades_id = request.args.get('grades_id')
    
    result = delete_grades_sql(grades_id)
    
    return jsonify({'success': result})
    

@app.route("/list_disciplinary", methods=["GET"])
def list_disciplinary():
    # DRO Only
    
    student_id = request.args.get('student_id')
    
    if student_id:
        result = list_disciplinary_by_student_id(student_id)
    else:
        result = list_all_disciplinary_sql()
    
    return jsonify(result) if result else jsonify([])

@app.route("/add_disciplinary", methods=["POST"])
def add_disciplinary():
    # DRO Only
    
    data = request.get_json()
    
    student_id = data.get('student_id')
    staff_id = data.get('staff_id')
    date = data.get('date')
    descriptions = data.get('descriptions')
    
    result = add_disciplinary_sql(student_id, staff_id, date, descriptions)
    
    return jsonify({'success': result})

@app.route("/modify_disciplinary", methods=["PUT"])
def modify_disciplinary():
    # DRO Only
    
    data = request.get_json()
    
    disciplinary_id = data.get('disciplinary_id')
    descriptions = data.get('descriptions')
    
    result = modify_disciplinary_sql(disciplinary_id, descriptions)
    
    return jsonify({'success': result})

@app.route("/delete_disciplinary", methods=["DELETE"])
def delete_disciplinary():
    # DRO Only
    
    disciplinary_id = request.args.get('disciplinary_id')
    
    result = delete_disciplinary_sql(disciplinary_id)
    return jsonify({'success': result})

@app.route("/guardian_children", methods=["DELETE"])
def guardian_children():
    # guardian Only
    
    guardian_id = request.args.get('GET')
    
    result = get_student_information_by_guardian_id(guardian_id)
    
    return result

@app.route("/list_student", methods=["GET"])
def list_student():
    # ARO and DRO
    
    result = list_student_sql()
    return jsonify(result) if result else jsonify([])

@app.route("/list_course", methods=["GET"])
def list_course():
    # ARO only
    
    result = list_course_sql()
    return jsonify(result) if result else jsonify([])

@app.route("/list_staff", methods=["GET"])
def list_staff():
    # DRO only
    
    result = list_staff_sql()
    return jsonify(result) if result else jsonify([])

if __name__ == "__main__":
    app.run(debug=True, port=5000)
