from flask import Blueprint, Flask, request, render_template, session, redirect, jsonify
from flask_session import Session
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from ..models.user import User
from ..models.stock import Stock
from ..models.transaction import Transaction
from ..extensions import db

#WTFORMS
from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField, RadioField, DecimalField)
from wtforms.validators import InputRequired, NumberRange

class AddStocksForm(FlaskForm):
    name = StringField("Stock Name", validators=[InputRequired()])
    brand = StringField("Brand")
    regular_price = DecimalField("Price")
    description = TextAreaField("Product Description")
    quantity = IntegerField("Quantity", validators=[InputRequired(),NumberRange(min=1)])
    barcode = StringField("Barcode")


stocks_mgmt = Blueprint('stocks_mgmt', __name__)



@stocks_mgmt.route("/stocks", methods=["GET"])
def stocks():
    stocks =  db.session.query(Stock)

    #WTFORMS
    addStocksForm = AddStocksForm()

    for stock in stocks:
        print(stock.name)
    return render_template("stocks.html", stocks=stocks, addStocksForm=addStocksForm)


#Function in flask route to handle form submission
@stocks_mgmt.route("/form_request_addstock", methods=["POST"])
def form_request_addstock():
    #WTFORMS
    addStocksForm = AddStocksForm()

    if addStocksForm.validate_on_submit():
        stock = Stock(name=addStocksForm.name.data, brand=addStocksForm.brand.data, regular_price=addStocksForm.regular_price.data, description=addStocksForm.description.data, quantity=addStocksForm.quantity.data, barcode=addStocksForm.barcode.data)
        transaction = Transaction(product_id = stock.id, quantity = stock.quantity, price = stock.regular_price, type = "Add Stock", transaction_date = datetime.now)
        db.session.add(stock)
        db.session.add(transaction)
        db.session.commit()
        return redirect("/stocks")
    else:
        return render_template("stocks.html", addStocksForm=addStocksForm)
    
@stocks_mgmt.route("/form_request_removestock", methods=["POST"])
def form_request_removestock():
    id = request.form.get("removestockid");
    stock = Stock.query.filter_by(id=id).first()
    stock.is_deleted = True
    stock.deleted_at = datetime.utcnow()
    db.session.commit()
    return redirect("/stocks")


    



