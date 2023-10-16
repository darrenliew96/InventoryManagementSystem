from flask import Blueprint, Flask, request, render_template, session, redirect, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from flask_sqlalchemy import SQLAlchemy
from ..helpers import login_required

from ..models.user import User
from ..extensions import db

user_settings = Blueprint('user_settings', __name__)

#user settings page
@user_settings.route("/settings")
@login_required
def settings():
    user = db.session.execute(db.select(User).filter_by(id=session["user_id"])).scalar_one()
    print(user.email)

    return render_template("settings.html", useremail=user.email, username=user.username)

@user_settings.route("/form_request_changeemail", methods=["POST"])
@login_required
def form_request_changeemail():
    newemail = request.form.get('newemail')
    confirmpasswordemail = request.form.get('currentpasswordemail')

    if not newemail:
        error_message = "New email cannot be empty!"
        return jsonify({'error': error_message})
    if not confirmpasswordemail:
        error_message = "Please enter confirmation password!"
        return jsonify({'error': error_message})

    #check if email already exist, pass exception is none was found, else return error message
    try:
        email = db.session.execute(db.select(User).filter_by(email=newemail)).scalar_one()
    
    except NoResultFound:
        pass

    else:
        error_message = "Email existed! Please try another email!"
        return jsonify({'error': error_message})
    
        
    #query for username to be logged in
    user = db.session.execute(db.select(User).filter_by(id=session["user_id"])).scalar_one()

    
    if check_password_hash(user.password ,confirmpasswordemail) is False:
        error_message = "Confirmation Password Error!"
        return jsonify({'error': error_message})
    
    else:
        user.email = newemail
        db.session.commit()
        return jsonify({'success': True, 'success_text': "Email successfully changed!"})
    


@user_settings.route("/form_request_changepassword", methods=['POST'])
@login_required
def form_request_changepassword():
    oldpassword = request.form.get('oldpassword')
    newpassword = request.form.get('newpassword')
    confirmpassword = request.form.get('confirmpassword')

    if not oldpassword:
        error_message = "Old password cannot be empty!"
        return jsonify({'error': error_message})
    if not newpassword:
        error_message = "New password cannot be empty!"
        return jsonify({'error': error_message})
    if not confirmpassword:
        error_message = "Confimation password cannot be empty!"
        return jsonify({'error': error_message})
    
    if oldpassword == newpassword:
        error_message = "New Password and Old Password cannot be the same!"
        return jsonify({'error': error_message})

    if confirmpassword != newpassword:
        error_message = "New Password and Confimation Password is not the same!"
        return jsonify({'error': error_message})
    
    
    #Query DB ORM for that specific logged in ID
    user = db.session.execute(db.select(User).filter_by(id=session["user_id"])).scalar_one()
    
    #Check for authenticity of current user password, if not return false and JSON data
    if check_password_hash(user.password, oldpassword) is False:
        error_message = "Old password is invalid, Please input correct password!"
        return jsonify({'error': error_message})

    #Change the password of the usercurrent session also make sure confirmation password is same as the new password
    if newpassword == confirmpassword:
        user.password = generate_password_hash(newpassword)
        db.session.commit()
        return jsonify({'success': True, 'success_text': "Password successfully changed!"})

@user_settings.route("/form_request_changeusername", methods=["POST"])
@login_required
def form_request_changeusername():
    newusername = request.form.get("newusername")
    confirmpasswordusername = request.form.get("currentpasswordusername")

    if not newusername:
        error_message = "New username cannot be empty!"
        return jsonify({'error': error_message})
    if not confirmpasswordusername:
        error_message = "Please enter confirmation password!"
        return jsonify({'error': error_message})

     #check if username already exist, pass exception is none was found, else return error message
    try:
        username = db.session.execute(db.select(User).filter_by(username=newusername)).scalar_one()
    
    except NoResultFound:
        pass

    else:
        error_message = "Username existed! Please try another username!"
        return jsonify({'error': error_message})
    

    #query for username to be logged in
    user = db.session.execute(db.select(User).filter_by(id=session["user_id"])).scalar_one()

    
    if check_password_hash(user.password ,confirmpasswordusername) is False:
        error_message = "Confirmation Password Error!"
        return jsonify({'error': error_message})
    
    else:
        user.username = newusername
        db.session.commit()
        return jsonify({'success': True, 'success_text': "Username successfully changed!"})