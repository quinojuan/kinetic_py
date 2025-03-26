from flask import Flask
from flask_cors import CORS
from .db import pool
from .read_excel_sheet import leer_hojas_excel
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'you-will-never-guess'
CORS(app, origins=["http://localhost:5173"])

from .routes import *