from sql_method import *

def login_controller(data):
    # for all role to login
    id = data.args.get('id')
    password = data.args.get('password')
    
    result = get_password_hash_by_id(id)
    if not result:
        return None # user not exist
    
    #......
    
    return None

def check_information_controller(data):
    # for student or guardian to check personal information
    role = data.args.get('role')
    id = data.args.get('id')
    
    #get_student_information_by_student_id()
    #get_guardian_information_by_guardian_id()
    
    return None
    
def maintain_information_controller(data):
    # for student or guardian to maintain personal information
    role = data.args.get('role')
    id = data.args.get('id')
    #other data
    
    #update_student_information_sql()
    #update_guardian_information_sql()
    
    return None

def list_grades_controller():
    # for ARO to list out all grades (or by student id, course id or term)
    #list_all_grades_sql()
    #list_grades_by_student_id()
    #list_grades_by_course_id()
    #list_grades_by_term()
    
    return None

def list_disciplinary_controller():
    # for DRO to list out all disciplinary (or by student id)
    #list_all_disciplinary_sql()
    #list_grades_by_student_id()
    
    return None