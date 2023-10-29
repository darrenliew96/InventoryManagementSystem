from flask import Flask
from flask_session import Session
from flask_migrate import Migrate
from flask_qrcode import QRcode
import os


from .extensions import db

#Routes
from .routes.user_page import user_page
from .routes.user_settings import user_settings
from .routes.api import api
from .routes.stocks_mgmt import stocks_mgmt
from .routes.transactions_mgmt import transactions_mgmt

def create_app():
    #Configure Flask App
    app=Flask(__name__)
    QRcode(app)

    #Configure Blueprints
    app.register_blueprint(user_page)
    app.register_blueprint(api)
    app.register_blueprint(user_settings)
    app.register_blueprint(stocks_mgmt)
    app.register_blueprint(transactions_mgmt)

    if __name__ == "__main__":
        app.run(debug=True)

    # Configure SQLALCHEMY
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ims.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    #configure Secret Key for WTFORM CSRF protection
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY

    db.init_app(app)
    migrate = Migrate(app, db)
    

    with app.app_context():
        db.create_all()

    #Configure Flask Session
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    return app