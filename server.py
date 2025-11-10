from flask import Flask, request, jsonify, send_from_directory
from controller import *
from sql_method_student_guardian import *
from sql_method_ARO_DRO import *
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'helloxixixixixixixixixixixixi'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # Token exp in 1 hour

jwt = JWTManager(app)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')  # 前端需要提供角色：'student', 'guardian', 'staff'

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
