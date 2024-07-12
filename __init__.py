from flask import Flask
import firebase_admin
from firebase_admin import credentials, firestore

firebase_app = None

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.secret_key = 'supersecretkey' 

    cred = credentials.Certificate('app/storify-62fc5-firebase-adminsdk-24tz0-4c48c0f022.json')
    global firebase_app
    firebase_app = firebase_admin.initialize_app(cred)
    app.firestore_db = firestore.client()

    with app.app_context():
        from .routes import main_bp
        app.register_blueprint(main_bp)

    return app

if __name__ == '__main__':
    app.run()