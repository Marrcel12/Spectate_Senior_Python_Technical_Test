from flask import Flask

from .database import DATABASE_URL


def create_app(conn=None):
    app = Flask(__name__)
    from .main import main_bp

    app.register_blueprint(main_bp, url_prefix="/api")
    if conn is not None:
        app.config["conn_url"] = conn
    else:
        app.config["conn_url"] = DATABASE_URL
    return app
