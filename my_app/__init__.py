from flask import Flask, request, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456789@localhost/StudentManagementDB?charset=utf8mb4"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=120)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '1fabace46bcf5b6eebda3de7'

db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = 'info'

from my_app import routes
from my_app import admin
