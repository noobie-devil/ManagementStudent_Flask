from my_app import app
from flask import Flask, render_template, redirect, url_for, flash, request, session,json
from my_app.models import *
from my_app.forms import LoginForm
from my_app import db
from flask_login import login_user, logout_user, login_required, current_user
from my_app import admin


@app.route('/', methods=('GET', 'POST'))
@app.route('/login', methods=('GET', 'POST'))
def login_page():
	if current_user.is_authenticated:
		logout_user()
		flash("Phiên đăng nhập của bạn đã kết thúc!!!", category='info')
	form = LoginForm()
	if form.validate_on_submit():
		attempted_user = Account.query.filter_by(username=form.username.data).first()
		if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
			if attempted_user.is_admin():
				login_user(attempted_user)
				flash(f'Đăng nhập thành công !!!', category='success')
				return redirect(url_for('admin.index'))
			if attempted_user.is_student():
				login_user(attempted_user)
				flash(f'Đăng nhập thành công !!!', category='success')
				return redirect(url_for('_student.index'))
			if attempted_user.is_teacher():
				login_user(attempted_user)
				flash(f'Đăng nhập thành công !!!', category='success')
				return redirect(url_for('_teacher.index'))
			session.permanent = True
		else:
			flash('Tên người dùng hoặc mật khẩu không đúng! Vui lòng thử lại', category='danger')
	return render_template('login.html', form=form)

@app.route('/logout')
def logout():
	logout_user()
	flash("Bạn đã đăng xuất!", category='info')
	return redirect(url_for('login_page'))

