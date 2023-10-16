from flask import Blueprint, Flask, request, render_template, session, redirect, jsonify
from flask_session import Session
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from flask_sqlalchemy import SQLAlchemy


from ..models.transaction import Transaction
from ..extensions import db

transactions_mgmt = Blueprint("transactions_mgmt", __name__)

@transactions_mgmt.route("/transactions", methods=["GET"])
def transactions():
    return render_template("transactions.html")