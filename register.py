from flask import Blueprint, Flask, request, render_template, session, redirect, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from flask_sqlalchemy import SQLAlchemy

register = Blueprint('register', __name__, template_folder='templates')

