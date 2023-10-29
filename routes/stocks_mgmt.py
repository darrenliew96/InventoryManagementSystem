from flask import Blueprint, Flask, request, render_template, session, redirect, jsonify
from flask_session import Session
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
    qr_data = StringField("QR Data")

class EditStocksForm(FlaskForm):
    name = StringField("Stock Name", validators=[InputRequired()])
    brand = StringField("Brand")
    regular_price = DecimalField("Price")
    description = TextAreaField("Product Description")
    quantity = IntegerField("Quantity", validators=[InputRequired(),NumberRange(min=1)])
    barcode = StringField("Barcode")
    qr_data = StringField("QR Data")


stocks_mgmt = Blueprint('stocks_mgmt', __name__)



@stocks_mgmt.route("/stocks", methods=["GET"])
def stocks():
    stocks =  db.session.query(Stock)

    #WTFORMS
    addStocksForm = AddStocksForm()
    editStocksForm = EditStocksForm()

    return render_template("stocks.html", stocks=stocks, addStocksForm=addStocksForm, editStocksForm=editStocksForm)


#Function in flask route to handle form submission
@stocks_mgmt.route("/form_request_addstock", methods=["POST"])
def form_request_addstock():
    #WTFORMS
    addStocksForm = AddStocksForm()

    if addStocksForm.validate_on_submit():
        #Stock DB Logics
        stock = Stock(name=addStocksForm.name.data, brand=addStocksForm.brand.data, regular_price=addStocksForm.regular_price.data, description=addStocksForm.description.data, quantity=addStocksForm.quantity.data, barcode=addStocksForm.barcode.data, qr_data=addStocksForm.qr_data.data)
        db.session.add(stock)

        #commit DB update for stocks
        db.session.commit()

        #Transaction DB Logics
        transaction = Transaction(product_id = stock.id, type="Add Stock", quantity = stock.quantity, price = stock.regular_price, transaction_date = datetime.now())
        db.session.add(transaction)

        #commit DB update for transaction
        db.session.commit()
        return redirect("/stocks")
    else:
        return redirect("/stocks")
    
@stocks_mgmt.route("/form_request_removestock", methods=["POST"])
def form_request_removestock():
    id = request.form.get("removestockid");
    stock = Stock.query.filter_by(id=id).first()
    stock.is_deleted = True
    stock.deleted_at = datetime.utcnow()
    transaction = Transaction(product_id = stock.id, type="Remove Stock", quantity = stock.quantity, price = stock.regular_price, transaction_date = datetime.now())
    db.session.add(transaction)
    db.session.commit()
    return redirect("/stocks")

@stocks_mgmt.route("/form_request_editstock", methods=["POST"])
def form_request_editstock():
    id = request.form.get("editstockid")
    print(id)
    stock = Stock.query.filter_by(id=id).first()

    editStocksForm = EditStocksForm()

    if editStocksForm.validate_on_submit():
        stock.name = editStocksForm.name.data
        stock.brand = editStocksForm.brand.data
        stock.regular_price = editStocksForm.regular_price.data
        stock.description = editStocksForm.description.data
        stock.quantity = editStocksForm.quantity.data
        stock.barcode = editStocksForm.barcode.data
        stock.qr_data = editStocksForm.qr_data.data
        db.session.commit()

        transaction = Transaction(product_id = stock.id, type="Edit Stock", quantity = stock.quantity, price = stock.regular_price, transaction_date = datetime.now())
        db.session.add(transaction)
        db.session.commit()

        return redirect("/stocks")
    else:
        return redirect("/stocks")


    



