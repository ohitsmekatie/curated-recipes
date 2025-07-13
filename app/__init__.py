from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = "super-secret-postmodern-key-2025"
    from .routes import main
    app.register_blueprint(main)
    return app
