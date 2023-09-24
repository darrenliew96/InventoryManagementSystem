from flask import Flask, request, render_template, session, redirect, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from helpers import login_required

db = SQLAlchemy()
#Configure Flask App
app=Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

# Configure SQLALCHEMY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ims.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String)
    email = db.Column(db.String(100), unique=True)
    date_joined = db.Column(db.Date, default=datetime.utcnow)

with app.app_context():
    db.create_all()


#Configure Flask Session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#Main index Route
@app.route("/")
@login_required
def hello_world():
    
    return render_template("login.html")


#From CS50 login method
@app.route("/login", methods=["GET","POST"])
def login():
    session.clear()
    return render_template("login.html")

#Define AJAX Form request route
@app.route("/form_request", methods=["POST"])
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
        user = db.session.execute(db.select(Users).filter_by(username=username)).scalar_one()
    except NoResultFound:
        error_message = "Invalid Username!"
        return jsonify({'error': error_message})
    
    #Check for password hash using internal hash function
    if not check_password_hash(user.password, request.form.get("password")):
        error_message = "Invalid Username / Password!"
        return jsonify({'error': error_message})

    session["user_id"] = user.id
    return jsonify({'success': True})

@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html")
    

@app.route("/form_request_register", methods=["POST"])
def form_request_register():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    #Get input and disallow blank input
    if not username:
        error_message = "Username cannot be empty!"
        return jsonify({'error': error_message})
    if not password:
        error_message = "Password cannot be empty!"
        return jsonify({'error': error_message})
    if not email:
        error_message = "Email cannot be empty!"
        return jsonify({'error': error_message})
    
    print(Users.query.filter_by(username=username).first())

    #Query for username and email if its available, otherwise return error
    if Users.query.filter_by(username=username).first() is not None:
        error_message = "Username Exist!"
        return jsonify({'error': error_message})
    elif Users.query.filter_by(email=email).first() is not None:
        error_message = "Email Exist!"
        return jsonify({'error': error_message})
    
    #Hashed password using flask Werkzerg library
    hashedPassword = generate_password_hash(password)

    #Insert user and password into SQL tables after checks
    newuser = Users(username = username, password = hashedPassword, email = email)

    #Execute Query using ORM
    db.session.add(newuser)
    db.session.commit()

    #Return sucess to AJAX and refresh the page to main page
    return jsonify({'success': True})

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect("/")