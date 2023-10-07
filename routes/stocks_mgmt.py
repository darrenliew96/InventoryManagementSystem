from flask import Blueprint, Flask, request, render_template, session, redirect, jsonify
from flask_session import Session
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from flask_sqlalchemy import SQLAlchemy


from ..models.user import Users
from ..extensions import db

stocks_mgmt = Blueprint('stocks_mgmt', __name__)


@stocks_mgmt.route("/stocks", methods=["GET"])
def stocks():
    return render_template("stocks.html")