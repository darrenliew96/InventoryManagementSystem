from flask import Blueprint, Flask, request, render_template, session, redirect
from flask_session import Session

from .extensions import db
from .routes.user_page import user_page
from .routes.user_settings import user_settings
from .routes.api import api

def create_app():
    #Configure Flask App
    app=Flask(__name__)

    #Configure Blueprints
    app.register_blueprint(user_page)
    app.register_blueprint(api)
    app.register_blueprint(user_settings)

    if __name__ == "__main__":
        app.run(debug=True)

    # Configure SQLALCHEMY
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ims.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    #Configure Flask Session
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    return app