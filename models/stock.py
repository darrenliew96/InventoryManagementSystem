from ..extensions import db
from datetime import datetime


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    brand = db.Column(db.String)
    SKU = db.Column(db.String)
    description = db.Column(db.String)
    barcode = db.Column(db.String)
    qr_data = db.Column(db.String)
    regular_price = db.Column(db.Float)
    discount_price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    picture_id = db.Column(db.Integer, db.ForeignKey("stock_picture.id"))
    is_deleted = db.Column(db.Boolean, default=False)
    created_at= db.Column(db.DateTime, default=datetime.utcnow)
    modified_at= db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at= db.Column(db.DateTime)


class Stock_picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    is_deleted = db.Column(db.Boolean, default=False)
    created_at= db.Column(db.DateTime, default=datetime.utcnow)
    modified_at= db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at= db.Column(db.DateTime)
