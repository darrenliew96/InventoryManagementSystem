from ..extensions import db
from datetime import datetime

from ..models.stock import Stock
from ..models.user import User

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("stock.id"))
    transaction_date = db.Column(db.Date, default=datetime.utcnow)
    type = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float)
    agent_id = db.Column(db.Integer, db.ForeignKey("agent.id"))
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
    is_deleted = db.Column(db.Boolean, default=False)
    created_at= db.Column(db.DateTime, default=datetime.utcnow)
    modified_at= db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at= db.Column(db.DateTime)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
    order_status = db.Column(db.String)
    order_tracking_number = db.Column(db.String)
    order_delivered_at = db.Column(db.DateTime)
    is_deleted = db.Column(db.Boolean, default=False)
    created_at= db.Column(db.DateTime, default=datetime.utcnow)
    modified_at= db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at= db.Column(db.DateTime)
