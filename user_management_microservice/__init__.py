import os

from flask import Flask
from flask_jwt_extended import JWTManager

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'UMMS.sqlite'),
        JWT_SECRET_KEY = 'Re3$52e@#qwi@#q2e3452ej1*us450'
    )
    
    jwt = JWTManager(app)
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    os.makedirs(app.instance_path, exist_ok=True)
    
    @app.route('/')
    def index():
        return "<h1>User Management Microservice</h1>"
      
    from . import init_db
    init_db.init_app(app)
    
    from . import functions
    app.register_blueprint(functions.auth_bp)
    app.register_blueprint(functions.users_bp)
    
    return app
  
  # flask --app user_management_microservice run --debug