import os

from flask import Flask, render_template
import logging

class Config(object):
    """生成环境配置"""
    SECRET_KEY = 'secret key'
def create_app():
    app = Flask('flask-student-information-management-system')
    app.config.from_object(Config)
    register_blueprint(app)
    return app

def register_blueprint(app):
    from info.index import index_bp
    from info.auth import auth_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(index_bp)

