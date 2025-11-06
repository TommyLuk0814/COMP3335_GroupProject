from flask import Flask, request, jsonify, send_from_directory
from controller import *
from sql_method import *

app = Flask(__name__)

@app.route("/login", methods=["POST"])
def login():
    # all role
    data = request
    
    result = login_controller(data)
    
    return None

@app.route("/check_information", methods=["POST"])
def check_information():
    # student and guardian
    data = request
    
    result = check_information_controller(data)
    
    return None

@app.route("/maintain_information", methods=["POST"])
def maintain_information():
    # student and guardian
    data = request
    
    result = maintain_information_controller(data)
    
    return None

@app.route("/check_grades", methods=["POST"])
def check_grades():
    # student, guardian
    
    result = list_grades_by_student_id()
    
    return None

@app.route("/check_disciplinary", methods=["POST"])
def check_disciplinary():
    # student, guardian
    
    result = list_disciplinary_by_student_id()
    
    return None

@app.route("/list_grades", methods=["POST"])
def list_grades():
    # ARO Only
    
    result = list_grades_controller()
    
    return None

@app.route("/add_grades", methods=["POST"])
def add_grades():
    # ARO Only
    
    result = add_grades_sql()
    
    return None

@app.route("/modify_grades", methods=["POST"])
def modify_grades():
    # ARO Only
    
    result = modify_grades_sql()
    
    return None

@app.route("/delete_grades", methods=["POST"])
def delete_grades():
    # ARO Only
    
    result = delete_grades_sql()
    
    return None

@app.route("/list_disciplinary", methods=["POST"])
def list_disciplinary():
    # DRO Only
    
    result = list_disciplinary_controller()
    
    return None

@app.route("/add_disciplinary", methods=["POST"])
def add_disciplinary():
    # DRO Only
    
    result = add_disciplinary_sql()
    
    return None

@app.route("/modify_disciplinary", methods=["POST"])
def modify_disciplinary():
    # DRO Only
    
    result = modify_disciplinary_sql()
    
    return None

@app.route("/delete_disciplinary", methods=["POST"])
def delete_disciplinary():
    # DRO Only
    
    result = delete_disciplinary_sql()
    
    return None