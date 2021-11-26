from flask import Flask, request, render_template, app
from flask_babelex import Babel
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from datetime import timedelta
import cloudinary

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456789@localhost/StudentManagementDB?charset=utf8mb4"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=120)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '1fabace46bcf5b6eebda3de7'
app.config['CLOUDINARY_INFO'] = {
	"cloud_name": "dsqpeicna",
	"api_key": "512116696657438",
	"api_secret": "gGxCS4T2Bv1iZG9Vbh68x7NVq6g",

}
db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = 'info'

cloudinary.config(cloud_name=app.config["CLOUDINARY_INFO"]["cloud_name"], api_key=app.config["CLOUDINARY_INFO"]["api_key"], api_secret=app.config["CLOUDINARY_INFO"]["api_secret"])


from my_app import routes
from my_app import admin

babel = Babel(app=app)

@babel.localeselector
def get_locale():
	return 'vi'
# can_view_details
# can_export
# edit_modal
# details_modal
# column_filters = ['name','']
# column_searchable_list = ['name']