from ..extensions import db

class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itemName = db.Column(db.String(100))
    itemQuantity = db.Column(db.Integer)
    itemDescription = db.Column(db.String)
    itemLocation = db.Column(db.String)
    itemPrice = db.Column(db.Numeric(precision=100, scale=2))