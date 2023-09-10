from flask import Flask, request, render_template, session, redirect
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from helpers import login_required

db = SQLAlchemy()
#Configure Flask App
app=Flask(__name__)

# Configure SQLALCHEMY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ims.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
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

    if request.method == "POST":
       if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            error = "Must Provide Username!"
            return render_template("login.html", error = error)

        # Ensure password was submitted
        elif not request.form.get("password"):
            error = "Must Provide Password!"
            return render_template("login.html", error = error)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            error = "Invalid username or password!"
            return render_template("login.html", error=error)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")
       
    # if GET request, then show login page
    else:
        return render_template("login.html")