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
				if current_user.active == 0:
					return redirect(url_for('_confirmStudent.index'))
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

@app.route('/forgot-password', methods=('GET', 'POST'))
def forgot():
	if request.method == "POST":
		email = request.form.get('email')
		moreinfo_user = MoreInfo.query.filter_by(email = email).first()
		if moreinfo_user is None:
			return render_template('forgot-password.html')
		else:
			attempted_user = Account.query.filter_by(user_id=moreinfo_user.user_id).first()
			login_user(attempted_user)
		return render_template('create-new-password.html', email = current_user.user_id)
	return render_template('forgot-password.html')

@app.route('/forgot-password/change', methods=('GET', 'POST'))
def forgot_change():
	if request.method == "POST":
		new_password = request.form.get('new_password')
		confirm_new_password = request.form.get('confirm_new_password')
		if new_password == confirm_new_password:
			attempted_user = Account.query.filter_by(user_id=current_user.user_id).first()
			attempted_user.password = confirm_new_password
			db.session.commit()
			flash(f'Đổi mật khẩu thành công!', category='success')
		else:
			flash(f'Byebye!', category='danger')
	logout_user()
	return redirect(url_for('login_page'))