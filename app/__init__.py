from flask import Flask
from .config import Config
from .extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.routes import department_routes # 在这里添加所有的 routes
    app.register_blueprint(department_routes.bp)

    return app