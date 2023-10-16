from flask import Blueprint, Flask, request, render_template, session, redirect, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from flask_sqlalchemy import SQLAlchemy

from ..models.user import User
from ..extensions import db

user_page = Blueprint('user_page', __name__)


#From CS50 login method
@user_page.route("/login", methods=["GET","POST"])
def login():
    session.clear()
    return render_template("login.html")

#Define AJAX Form request route
@user_page.route("/form_request", methods=["POST"])
def form_request():
    username = request.form.get("username")
    password = request.form.get("password")

    # Ensure username was submitted
    if not username:
        error_message = "Must Provide Username!"
        return jsonify({'error': error_message})

    # Ensure password was submitted
    elif not password:
        error_message = "Must Provide Password!"
        return jsonify({'error': error_message})

    # Query database for username using SQL alchemy ORM (Scalar one) TRY
    try:
        user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one()
    except NoResultFound:
        error_message = "Invalid Username!"
        return jsonify({'error': error_message})
    
    #Check for password hash using internal hash function
    if not check_password_hash(user.password, request.form.get("password")):
        error_message = "Invalid Username / Password!"
        return jsonify({'error': error_message})

    #Create a new session using current user id
    session["user_id"] = user.id
    return jsonify({'success': True})


@user_page.route("/register", methods=["GET"])
def register():
    return render_template("register.html")
    
@user_page.route("/form_request_register", methods=["POST"])
def form_request_register():
    fullname = request.form.get("fullname")
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    #Get input and disallow blank input
    if not fullname:
        error_message = "Name cannot be empty!"
        return jsonify({'error': error_message})
    if not username:
        error_message = "Username cannot be empty!"
        return jsonify({'error': error_message})
    if not password:
        error_message = "Password cannot be empty!"
        return jsonify({'error': error_message})
    if not email:
        error_message = "Email cannot be empty!"
        return jsonify({'error': error_message})

    #Query for username and email if its available, otherwise return error
    if User.query.filter_by(username=username).first() is not None:
        error_message = "Username Exist!"
        return jsonify({'error': error_message})
    elif User.query.filter_by(email=email).first() is not None:
        error_message = "Email Exist!"
        return jsonify({'error': error_message})
    
    #Hashed password using flask Werkzerg library
    hashedPassword = generate_password_hash(password)

    #Insert user and password into SQL tables after checks
    newuser = User(fullname=fullname, username = username, password = hashedPassword, email = email)

    #Execute Query using ORM
    db.session.add(newuser)
    db.session.commit()

    #Return sucess to AJAX and refresh the page to main page
    return jsonify({'success': True})
