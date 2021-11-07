import os
from flask import Flask
from flask_cors import CORS
from dotenv import dotenv_values
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

config = dotenv_values(os.path.join(os.path.abspath(os.pardir), '.env'))

app.config['SECRET_KEY'] = config['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f"postgresql://{config['USER']}:{config['PASS']}@localhost:{config['PORT']}/{config['DATABASE']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = config['DEBUG']

db = SQLAlchemy(app)
