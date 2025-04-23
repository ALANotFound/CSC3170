from flask import Flask
from .config import Config
from .extensions import db
from flask_cors import CORS

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 启用CORS，支持跨域请求
    CORS(app, resources={r"/*": {"origins": "*"}})

    db.init_app(app)

    from .routes import department_routes # 在这里添加所有的 routes
    from .routes import doctor_routes
    from .routes import patient_routes
    from .routes import admission_routes
    from .routes import visit_routes
    from .routes import ward_routes
    from .routes import sta_routes
    app.register_blueprint(department_routes.bp)
    app.register_blueprint(doctor_routes.bp)
    app.register_blueprint(patient_routes.bp)
    app.register_blueprint(admission_routes.bp)
    app.register_blueprint(visit_routes.bp)
    app.register_blueprint(sta_routes.bp)
    app.register_blueprint(ward_routes.bp)

    return app
