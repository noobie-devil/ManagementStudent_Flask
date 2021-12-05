from flask_wtf import FlaskForm
from wtforms import fields
from wtforms.validators import Length, EqualTo, DataRequired, ValidationError, Regexp, Email
from my_app.models import *
from flask_admin.form import DatePickerWidget

class LoginForm(FlaskForm):
	username = fields.StringField(label='User Name:', validators=[DataRequired()])
	password = fields.PasswordField(label='Password:', validators=[Length(min=8, max=60), DataRequired()])
	submit = fields.SubmitField(label='Đăng nhập')

class TelephoneForm(FlaskForm):
    country_code = fields.IntegerField(label='Country Code', validators=[DataRequired()])
    area_code    = fields.IntegerField(label='Area Code/Exchange', validators=[DataRequired()])
    number       = fields.StringField('Number')

class CreateUserForm(FlaskForm):
	full_name = fields.StringField(label='Họ và tên', validators=[Length(max=50), DataRequired()])
	gender = fields.SelectField("Giới tính", choices=Gender.query.all(), validators=[DataRequired()])
	birthdate = fields.DateField("Ngày sinh", widget=DatePickerWidget(), validators=[DataRequired()])
	permanent_address = fields.StringField(label='Địa chỉ thường trú', validators=[Length(250), DataRequired()])
	home_town = fields.StringField(label='Quê quán', validators=[Length(50), DataRequired()])
	ethnic = fields.SelectField("Dân tộc", choices=Ethnic.query.all(), validators=[DataRequired()])
	nationality = fields.SelectField("Quốc tịch", choices=Nationality.query.all(), validators=[DataRequired()])
	note = fields.TextAreaField(validators=[Length(200)])

class UpdateInfoForm(FlaskForm):
	u_phone = fields.StringField(label="Điện thoại", validators=[Length(max=15), Regexp(regex='^[+-]?[0-9]$')])
	u_email = fields.StringField(label="Email", validators=[Email()])
	u_residence = fields.StringField(label="Địa chỉ", validators=[Length(max=100)])
	note = fields.TextAreaField(label="Ghi chú", validators=[Length(max=200)])
	contact_name = fields.StringField(label="Họ tên", validators=[Length(max=50)])
	contact_phone = fields.StringField(label="Điện thoại", validators=[Length(max=15), Regexp(regex='^[+-]?[0-9]$')])
	contact_residence = fields.StringField(label="Địa chỉ", validators=[Length(max=100)])
	submit = fields.SubmitField(label='Lưu')


class ChangePassForm(FlaskForm):
	o_password = fields.PasswordField(label='Old Password:', validators=[Length(min=8, max=60), DataRequired()])
	n_password = fields.PasswordField(label='New Password:', validators=[Length(min=8, max=60), DataRequired()])
	c_password = fields.PasswordField(label='Confirm New Password:', validators=[Length(min=8, max=60), DataRequired()])
	submit = fields.SubmitField(label='Đổi mật khẩu')
