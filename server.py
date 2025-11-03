from flask import Flask, request, jsonify, send_from_directory
import sql_method

app = Flask(__name__)

@app.route("/login", methods=["POST"])
def login():
    email = request.args.get('email')
    password = request.args.get('password')
    
    result = login_sql(email, passowrd)
    
    return None