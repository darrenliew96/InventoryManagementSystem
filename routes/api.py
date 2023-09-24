from flask import Flask, redirect, session, render_template, Blueprint
from ..helpers import login_required

api = Blueprint('api', __name__)

#Main index Route
@api.route("/")
@login_required
def index():
    return render_template("login.html")

#Logout Route
@api.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect("/")