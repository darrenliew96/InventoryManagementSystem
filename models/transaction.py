from ..extensions import db
from datetime import datetime

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transactionProductId = db.Column(db.Integer, db.ForeignKey("items.id"))
    transactionDate = db.Column(db.Date, default=datetime.utcnow)
