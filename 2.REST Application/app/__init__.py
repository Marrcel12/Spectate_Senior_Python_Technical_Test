from flask import Flask
from .database import initialize

def create_app():
    app = Flask(__name__)

    # with app.app_context():
    #     initialize()

    from .main import main_bp
    app.register_blueprint(main_bp, url_prefix='/api')

    return app
