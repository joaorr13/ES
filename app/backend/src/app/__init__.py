from flask import Flask
from config import Config
from flask_cors import CORS



def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    from app.routes.main import main as main_routes
    
    app.register_blueprint(main_routes)

    return app