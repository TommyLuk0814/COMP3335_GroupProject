from flask import Flask, request, jsonify, send_from_directory
from controller import *
from sql_method_student_guardian import *
from sql_method_ARO_DRO import *

app = Flask(__name__)

@app.route("/login", methods=["GET"])
def login():
    # all role
    email = request.args.get('email')
    
    result = login_controller(email)
    
    return result

@app.route("/check_information", methods=["GET"])
def check_information():
    # student and guardian
    data = request
    
    result = check_information_controller(data)
    
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
    
    result = list_grades_controller()
    
    return result

@app.route("/add_grades", methods=["POST"])
def add_grades():
    # ARO Only
    
    result = add_grades_sql()
    
    return result

@app.route("/modify_grades", methods=["PUT"])
def modify_grades():
    # ARO Only
    
    result = modify_grades_sql()
    
    return result

@app.route("/delete_grades", methods=["DELETE"])
def delete_grades():
    # ARO Only
    
    grades_id = request.args.get('grades_id')
    
    result = delete_grades_sql(grades_id)
    
    return result

@app.route("/list_disciplinary", methods=["GET"])
def list_disciplinary():
    # DRO Only
    
    result = list_disciplinary_controller()
    
    return result

@app.route("/add_disciplinary", methods=["POST"])
def add_disciplinary():
    # DRO Only
    
    result = add_disciplinary_sql()
    
    return result

@app.route("/modify_disciplinary", methods=["PUT"])
def modify_disciplinary():
    # DRO Only
    
    result = modify_disciplinary_sql()
    
    return result

@app.route("/delete_disciplinary", methods=["DELETE"])
def delete_disciplinary():
    # DRO Only
    
    disciplinary_id = request.args.get('disciplinary_id')
    
    result = delete_disciplinary_sql(disciplinary_id)
    
    return result

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
    
    return result

@app.route("/list_course", methods=["GET"])
def list_course():
    # ARO only
    
    result = list_course_sql()
    
    return result

@app.route("/list_staff", methods=["GET"])
def list_staff():
    # DRO only
    
    result = list_staff_sql()
    
    return result