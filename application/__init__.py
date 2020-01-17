from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import pymysql

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + getenv('MY_SQL_USER') + ':' + getenv('MY_SQL_PASS') + '@' + getenv('MY_SQL_HOST') + '/' + getenv('MY_SQL_DB')

db = SQLAlchemy(app)
bcrypt =Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

app.config['SECRET_KEY'] = 'vm43j09skpfk340wkfdof24doif40'

from application import routes
