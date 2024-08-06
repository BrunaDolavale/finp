from flask import Flask
from .config import Config
import pyrebase

app = Flask(__name__)
app.config.from_object(Config)

firebase = pyrebase.initialize_app(app.config['FIREBASE_CONFIG'])
db = firebase.database()

from app import views
