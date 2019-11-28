from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:aerojak@35.242.176.146/db'
db = SQLAlchemy(app)

from application import routes
