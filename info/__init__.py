import os

from flask import Flask, render_template



def create_app():
    app = Flask('flask-student-information-management-system')
    register_blueprint(app)
    return app

def register_blueprint(app):
    from info.index import index_bp
    from info.auth import auth_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(index_bp)

