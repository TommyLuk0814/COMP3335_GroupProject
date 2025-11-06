from sql_method_student_guardian import *
from sql_method_ARO_DRO import *

def login_controller(email):
    # for all role to login
    
    #get_student_information_by_email(email)
    #get_guardian_information_by_email(email)
    #get_aro_information_by_email(email)
    #get_dro_information_by_email(email)
    
    return None

def check_information_controller(data):
    # for student or guardian to check personal information
    role = data.args.get('role')
    
    #get_student_information_by_student_id()
    #get_guardian_information_by_guardian_id()
    
    return None
    
def maintain_information_controller(data):
    # for student or guardian to maintain personal information
    role = data.args.get('role')
    
    #update_student_information_sql()
    #update_guardian_information_sql()
    
    return None

def list_grades_controller():
    # for ARO to list out all grades (or by student id, course id or term)
    
    #list_all_grades_sql()
    #list_grades_by_student_id(student_id)
    #list_grades_by_course_id(course_id)
    #list_grades_by_term(term)
    
    return None

def list_disciplinary_controller():
    # for DRO to list out all disciplinary (or by student id)
    
    #list_all_disciplinary_sql()
    #list_grades_by_student_id(student_id)
    
    return None