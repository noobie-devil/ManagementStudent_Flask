from my_app.common import *
from flask import Markup
from my_app.my_base_view import MyBaseView

class MyAdminIndexView(AdminIndexView):
	def is_visible(self):
		return False
	@expose('/')
	def index(self):
		if not current_user.is_authenticated or current_user.is_admin() == False:
			flash('Please log in first...', category='danger')
			# next_url = request.url
			# login_url = '%s?next=%s' % (url_for('login_page'), next_url)
			return redirect(url_for('login_page'))
		return redirect(url_for('admin_index.index'))
		

user_form = {
	'user_id' : fields.HiddenField(label='user_id'),
	'full_name' : fields.StringField(label='Họ và tên', validators=[Length(max=50), DataRequired()]),
	'gender' : fields.SelectField("Giới tính", choices=Gender.query.all(), validators=[DataRequired()]),
	'birthdate' : fields.DateField("Ngày sinh", widget=DatePickerWidget(), validators=[DataRequired()]),
	'permanent_address' : fields.StringField(label='Địa chỉ thường trú', validators=[Length(min=0, max=250), DataRequired()]),
	'home_town' : fields.StringField(label='Quê quán', validators=[Length(min=0,max=50), DataRequired()]),
	'ethnic' : fields.SelectField("Dân tộc", choices=Ethnic.query.all(), validators=[DataRequired()]),
	'nationality' : fields.SelectField("Quốc tịch", choices=Nationality.query.all(), validators=[DataRequired()]),
	# 'note' : fields.TextAreaField(validators=[Length(max=200)]),
	'image': FileField("Hình ảnh", validators=[FileAllowed(['png','jpg','jpeg'], 'Invalid file type. Must be .png, .jpeg, .jpg')])
	}

def create_user(form, role):
	user_to_create = User(
		full_name=form.full_name.data,
		gender_id=Gender.query.filter_by(gender_name=form.gender.data).first().id,
		birthdate=form.birthdate.data, 
		permanent_address=form.permanent_address.data, 
		home_town=form.home_town.data, 
		ethnic_id=Ethnic.query.filter_by(ethnic_name=form.ethnic.data).first().id,
		nationality_id=Nationality.query.filter_by(nationality_name=form.nationality.data).first().id,
		# note=form.note.data,
		role_id=Role.query.filter_by(name=role).first().id
	)
	return user_to_create


class IndexView(MyBaseView):
	can_create = False
	can_delete = False
	can_edit = False
	column_searchable_list = ['full_name']

	column_list = ('id','role','full_name', 'gender', 'birthdate','permanent_address', 'home_town', 'ethnic', 'nationality', 'image', 'created_at')


	@expose('/')
	def index(self):
		return super(IndexView,self).index_view()

class CourseView(MyBaseView):
	form_excluded_columns = ('time','student')

	def on_model_change(self, form, Course, is_created):
		Course.time = form.start_year.data + '-' + form.end_year.data

class UserView(MyBaseView):

	def get_create_form(self):
		form = super(UserView, self).get_create_form()
		form.image = FileField("Hình ảnh", validators=[FileAllowed(['png','jpg','jpeg'], 'Invalid file type. Must be .png, .jpeg, .jpg')])
		return form


	def _image_formatter(view, context, model, name):
		if model.user.image:
			markupstring = "<img src='%s' alt='%s' width='100' heigh='100' >" % (model.user.image, model.user.image_id)
			return Markup(markupstring)
		else:
			return ""

	column_formatters = {
		'user.image': _image_formatter
	}
	# details_modal = True
	# can_view_details = True
	column_searchable_list = ['user.full_name']

	def on_form_prefill(self,form, id):
		user_model = self.session.query(self.model).filter(self.model.id == id).one()
		form.user_id = user_model.user_id
		form.full_name.data = user_model.user.full_name
		form.gender.data = user_model.user.gender.gender_name
		form.birthdate.data = user_model.user.birthdate
		form.permanent_address.data = user_model.user.permanent_address
		form.home_town.data = user_model.user.home_town
		form.ethnic.data = user_model.user.ethnic.ethnic_name
		form.nationality.data = user_model.user.nationality.nationality_name
		# form.note.data = user_model.user.note

	def update_model(self, form, model):
		user_to_update = self.session.query(User).get(model.user_id)
		user_to_update.full_name=form.full_name.data
		user_to_update.gender_id=Gender.query.filter_by(gender_name=form.gender.data).first().id
		user_to_update.birthdate=form.birthdate.data
		user_to_update.permanent_address=form.permanent_address.data
		user_to_update.home_town=form.home_town.data
		user_to_update.ethnic_id=Ethnic.query.filter_by(ethnic_name=form.ethnic.data).first().id
		user_to_update.nationality_id=Nationality.query.filter_by(nationality_name=form.nationality.data).first().id
		# user_to_update.note=form.note.data
		form.user_id = user_to_update.id

		return super(MyBaseView,self).update_model(form, model)

	def on_model_change(self, form, model, is_created):
		image = request.files['image']
		if image.filename != '':
			if is_created == False:
				if model.user.image_id != None:
					cloudinary.uploader.destroy(model.user.image_id, invalidate=True)
				info = cloudinary.uploader.upload(image)
				model.user.image = info['secure_url']
				model.user.image_id = info['public_id']
			
		if is_created and form.user_id:
			model.user_id = form.user_id
			
	def after_model_change(self, form, model, is_created):
		image = request.files['image']
		if is_created:
			if image.filename != '':
				user = User.query.filter_by(id=model.user_id).first()
				info = cloudinary.uploader.upload(image)
				user.image = info['secure_url']
				user.image_id = info['public_id']
				try:
					self.session.commit()
				except Exception as ex:
					self.session.rollback()

	def delete_model(self, model):
		
		try:
			account = self.session.query(Account).filter_by(user_id=model.user.id).first()
			if account != None:
				self.session.flush()
				self.session.delete(account)
				self.session.commit()
			user_info = self.session.query(MoreInfo).filter_by(user_id=model.user.id).first()
			if user_info != None:
				self.session.flush()
				self.session.delete(account)
				self.session.commit()
			user = self.session.query(User).filter_by(id=model.user.id).first()
			if user != None:
				self.session.flush()
				self.session.delete(user)
				self.session.commit()
			get_image = model.user.image_id
			self.on_model_delete(model)
			self.session.flush()
			self.session.delete(model)
			self.session.commit()
			if get_image != None:
				cloudinary.uploader.destroy(get_image, invalidate=True)
		except Exception as ex:
			if not self.handle_view_exception(ex):
				flash(gettext('Failed to delete record. %(error)s', error=str(ex)), 'error')
				log.exception('Failed to delete record.')

			self.session.rollback()

			return False
		else:
			self.after_model_delete(model)

		return True

class AdminView(UserView):
	form_excluded_columns = ('user', 'created_at')
	column_list = ('user.image','user.full_name', 'user.gender', 'user.birthdate', 'user.home_town', 'user.ethnic', 'user.nationality', 'user.role')
	form_extra_fields = user_form

	def create_model(self,form):
		user_to_create = create_user(form,'Admin')
		db.session.add(user_to_create)
		db.session.commit()
		form.user_id = user_to_create.id
		return super(AdminView,self).create_model(form)

	def after_model_change(self, form, model, is_created):
		if is_created:
			auto_create_account = Account()
			max_id = db.session.query(func.max(Administrator.id)).scalar()
			if max_id is None:
				auto_create_account.username = 'admin' + '{:0>3}'.format(1)
			else:
				if max_id != False:
					auto_create_account.username = 'admin' + '{:0>3}'.format(max_id+1)
			auto_create_account.user_id = model.user_id
			auto_create_account.password = '123456789'
			auto_create_account.role_id = model.user.role_id
			try:
				self.session.add(auto_create_account)
				self.session.commit()
			except Exception as ex:
				self.session.rollback()
			return super(AdminView,self).after_model_change(form,model,is_created)


class EducationalOfficeView(UserView):
	form_excluded_columns = ('user', 'created_at')
	column_list = ('user.image','user.full_name', 'user.gender', 'user.birthdate', 'user.home_town', 'user.ethnic', 'user.nationality', 'user.role')
	form_extra_fields = user_form

	def create_model(self,form):
		user_to_create = create_user(form,'Giáo vụ')
		db.session.add(user_to_create)
		db.session.commit()
		form.user_id = user_to_create.id
		return super(EducationalOfficeView,self).create_model(form)

	def after_model_change(self, form, model, is_created):
		if is_created:
			auto_create_account = Account()
			max_id = db.session.query(func.max(EducationalOffice.id)).scalar()
			if max_id is None:
				auto_create_account.username = 'PGV' + '{:0>3}'.format(1)
			else:
				if max_id != False:
					auto_create_account.username = 'PGV' + '{:0>3}'.format(max_id+1)
			auto_create_account.user_id = model.user_id
			auto_create_account.password = '123456789'
			auto_create_account.role_id = model.user.role_id
			try:
				self.session.add(auto_create_account)
				self.session.commit()
			except Exception as ex:
				self.session.rollback()
			return super(EducationalOfficeView,self).after_model_change(form,model,is_created)

class StudentView(UserView):
	form_excluded_columns = ('user', 'created_at','family_info', 'familyInfo','studentInClass','subjectTranscript')
	# column_list = ('user.image','student_code','user.full_name', 'user.gender', 'user.birthdate', 'user.home_town', 'user.ethnic', 'user.nationality')
	column_list = ('user.image','student_code','user.full_name', 'course.course_name', 'course.time')
	form_extra_fields = user_form

	

	def create_form(self):
		form = super(StudentView, self).create_form()
		max_id = db.session.query(func.max(Student.id)).scalar()
		if max_id is None:
			form.student_code.data = 'HS' + '{:0>5}'.format(1)
		else:
			if max_id != False:
				form.student_code.data = 'HS' + '{:0>5}'.format(max_id+1)
		
		return form


	def create_model(self,form):
		user_to_create = create_user(form,'Học sinh')
		db.session.add(user_to_create)
		db.session.commit()
		form.user_id = user_to_create.id
		return super(StudentView,self).create_model(form)

	def after_model_change(self, form, model, is_created):
		if is_created:
			auto_create_account = Account()
			auto_create_account.user_id = model.user_id
			auto_create_account.username = form.student_code.data
			auto_create_account.password = form.student_code.data[-4:] + '' + Course.query.filter_by(id=model.course_id).first().start_year
			auto_create_account.active = False
			auto_create_account.role_id = model.user.role_id
			try:
				self.session.add(auto_create_account)
				self.session.commit()
			except Exception as ex:
				self.session.rollback()
			return super(StudentView,self).after_model_change(form,model,is_created)

	# def get_create_form(self):
	# 	form = super(StudentView, self).get_create_form()
	# 	form.birthdate = fields.DateField("Năm", widget=DatePickerWidget(), format='%d-%m-%Y', validators=[DataRequired()])
	# 	return form

	# form_widget_args = {
	# 	'birthdate': {'data-date-format': 'YYYY'}
	# }
	


class TeacherView(UserView):

	form_excluded_columns = ('user', 'created_at', 'classInfo', 'teachingAssignment')

	column_list = ('user.image','teacher_code','subject','user.full_name', 'user.gender', 'user.role')
	
	form_extra_fields = user_form

	# def edit_form(self,obj):
	def create_form(self):
		form = super(TeacherView, self).create_form()
		max_id = db.session.query(func.max(Teacher.id)).scalar()
		if max_id is None:
			form.teacher_code.data = 'GV' + '{:0>4}'.format(1)
		else:
			if max_id != False:
				form.teacher_code.data = 'GV' + '{:0>4}'.format(max_id+1)
		
		return form

	
	def create_model(self,form):
		user_to_create = create_user(form,'Giáo viên')
		db.session.add(user_to_create)
		db.session.commit()
		form.user_id = user_to_create.id
		return super(TeacherView,self).create_model(form)

	def after_model_change(self, form, model, is_created):
		if is_created:
			auto_create_account = Account()
			auto_create_account.user_id = model.user_id
			auto_create_account.username = form.teacher_code.data
			auto_create_account.password = '123456789'
			auto_create_account.role_id = model.user.role_id
			try:
				self.session.add(auto_create_account)
				self.session.commit()
			except Exception as ex:
				self.session.rollback()
			return super(TeacherView,self).after_model_change(form,model,is_created)

def get_all_school_year():
    year = SchoolYear.query.all()
    return [(school_year.id, school_year.year) for school_year in year]

class ClassInfoView(MyBaseView):
	column_filters = [
		FilterEqual(column=ClassInfo.school_year_id, name='Năm học', options=get_all_school_year)
	]
	def get_query(self):
		# return super(ClassInfoView, self).get_query().filter(SchoolYear.active == True)
		return self.session.query(self.model).join(SchoolYear).filter(SchoolYear.active == True)
		# return self.session.query(self.model).filter(self.model.school_year.active==True)
		
	# def get_count_query(self):
	# 	return self.session.query(func.count('*')).filter(SchoolYear.active == True)
		# return self.session.query(func.count('*')).filter(self.model.school_year.active==True)

	form_excluded_columns = ('teacher', 'amount_std', 'student_In_Class')
	column_list = ('in_class.class_name', 'school_year', 'teacher.user.full_name', 'amount_std')


class AccountView(MyBaseView):
    # column_exclude_list = ['password']
    column_list = ('user.full_name','username', 'password_hash', 'active', 'created_at' )
    column_labels = dict(password_hash='Password Hashed', created_at='Ngày tạo')
    form_columns = ('user','username','password', 'role', 'active')
    form_extra_fields = {
        'password': fields.PasswordField(label='Password:',validators=[Length(min=8, max=60), DataRequired()])
    }
    def on_model_change(self, form, Account, is_created):
        if form.password.data:
        	Account.password = form.password.data

class PersonalInfoView(MyBaseView):

	list_template = 'admin/info.html'

	@expose('/')
	def info_view(self):
		return super(PersonalInfoView,self).list_view()

	edit_template = 'admin/edit_info.html'
	@expose('/edit', methods=['GET','POST'])
	def edit_view(self):
		update_info_form = UpdateInfoForm()
		if request.method == "POST":
		# if update_info_form.validate_on_submit():
			more_info = MoreInfo.query.filter_by(user_id=current_user.user_id).first()
			if more_info is not None:
				more_info.email = update_info_form.u_email.data
				more_info.phone = update_info_form.u_phone.data
				more_info.current_residence = update_info_form.u_residence.data
				more_info.note = update_info_form.note.data
			else: 
				more_info = MoreInfo(user_id=current_user.user_id,email=update_info_form.u_email.data,phone=update_info_form.u_phone.data,current_residence=update_info_form.u_residence.data,note=update_info_form.note.data,modified_at=datetime.now())
				db.session.add(more_info)
			db.session.commit()

			return redirect(url_for('.info_view'))
		more_info = MoreInfo.query.filter_by(user_id=current_user.user_id)
		return self.render('admin/edit_info.html', update_info_form=update_info_form, more_info=more_info)

	def render(self, template, **kwargs):
		more_info = MoreInfo.query.get(current_user.user_id)	
		if more_info is not None:
			kwargs['more_info'] = more_info
		return super(PersonalInfoView, self).render(template, **kwargs)


class TeachingAssignmentView(MyBaseView):
	column_list = ('subject','teacher.user.full_name', 'class_info', 'semester', 'school_year')
	form_excluded_columns = 'semester, transcript_info'
	# create_template = 'admin/create_teaching_assignment.html'

	def add_row(self, form,semester):
		model = TeachingAssignment()
		model.subject_id = form.subject.data.id
		model.teacher_id = form.teacher.data.id
		model.class_info_id = form.class_info.data.id
		model.school_year_id = form.school_year.data.id
		model.semester_id = semester.id
		
		return model

	def create_model(self,form):

		dicti = []
		semesters = Semester.query.all()
		for semester in semesters:
			try:
				model = self.add_row(form,semester)
				self.session.add(model)
				self.session.commit()
				dicti.append(model)
				
			except Exception as ex:
				if not self.handle_view_exception(ex):
					flash(gettext('Failed to create record. %(error)s', error=str(ex)), 'error')
					log.exception('Failed to create record.')

				self.session.rollback()

				return False
			else:
				self.after_model_change(form, model, True)

		return dicti


	# def create_subject_transcript(self,model):
	# 	model = SubjectTranscript()

	def after_model_change(self, form, model, is_created):
		if is_created:
			for std in model.class_info.student_In_Class:
				subj = SubjectTranscript()
				subj.student_id = std.student_id
				subj.transcript_info_id = model.id
				self.session.add(subj)
				self.session.commit()


class StudentInClassView(MyBaseView):
	def after_model_change(self, form, model, is_created):
		for teaching_assigment in self.session.query(TeachingAssignment).filter_by(class_info_id = model.class_info_id):
			subj = SubjectTranscript()
			subj.student_id = model.student_id
			subj.transcript_info_id = teaching_assigment.id
			self.session.add(subj)
			self.session.commit()

admin = Admin(app, name='UTE', index_view=MyAdminIndexView(), base_template='master.html', template_mode='bootstrap4')
admin.add_view(IndexView(User, db.session, name='Trang Chủ', url='/index-admin', endpoint='admin_index', menu_icon_type="ti", menu_icon_value="ti-home"))

admin.add_view(PersonalInfoView(MoreInfo, db.session, name="Thông tin cá nhân", url='/admin/info', endpoint='admin_info', menu_icon_type="ti", menu_icon_value="ti-pencil"))
admin.add_view(AccountView(Account, db.session, category="Quản lý tài khoản", name="Tài khoản"))
admin.add_view(MyBaseView(Role, db.session, category="Quản lý tài khoản", name="Thông tin quyền"))
admin.add_view(MyBaseView(MoreInfo, db.session, name="Danh sách liên hệ", menu_icon_type="ti", menu_icon_value="ti-id-badge"))

admin.add_view(StudentView(Student, db.session, name="Quản lý học sinh",  menu_icon_type="ti", menu_icon_value="ti-user"))

admin.add_view(TeacherView(Teacher, db.session, name="Giáo viên", menu_icon_type="ti", menu_icon_value="ti-user"))

admin.add_view(AdminView(Administrator, db.session, name="Quản trị viên", menu_icon_type="ti", menu_icon_value="ti-user"))

admin.add_view(EducationalOfficeView(EducationalOffice, db.session, name="Phòng giáo vụ", menu_icon_type="ti", menu_icon_value="ti-user"))

admin.add_view(MyBaseView(Class, db.session, category="Quản lý lớp học", name="Thông tin lớp học"))
admin.add_view(ClassInfoView(ClassInfo, db.session, category="Quản lý lớp học", name="Danh sách lớp học trong năm"))
admin.add_view(TeachingAssignmentView(TeachingAssignment, db.session, category="Quản lý lớp học",name="Phân công giảng dạy"))
admin.add_view(StudentInClassView(StudentInClass, db.session, category="Quản lý lớp học", name="Phân lớp"))

admin.add_view(MyBaseView(Subject, db.session, name="Quản lý môn học", menu_icon_type="ti", menu_icon_value="ti-book"))

admin.add_view(MyBaseView(ScoreType, db.session, category="Quản lý điểm", name="Thông tin bảng điểm"))
admin.add_view(MyBaseView(SubjectTranscript, db.session, category="Quản lý điểm", name="Điểm theo môn học"))


admin.add_view(MyBaseView(ResumeImageFields, db.session, name="Form hồ sơ nhập học", menu_icon_type="ti", menu_icon_value="ti-write"))

admin.add_view(MyBaseView(Semester, db.session, name="Học kỳ", menu_icon_type="ti", menu_icon_value="ti-notepad"))

admin.add_view(MyBaseView(SchoolYear, db.session, category='Năm học', name="Chỉnh sửa năm học", menu_icon_type="ti", menu_icon_value="ti-calendar"))
admin.add_view(CourseView(Course, db.session, category='Năm học', name="Chỉnh sửa niên khóa", menu_icon_type="ti", menu_icon_value="ti-calendar"))

admin.add_view(MyBaseView(Grade,db.session, category="Thông tin chung", name="Khối"))
admin.add_view(MyBaseView(Gender, db.session, category="Thông tin chung", name="Giới tính") )
admin.add_view(MyBaseView(Nationality, db.session, category="Thông tin chung", name="Quốc tịch"))
admin.add_view(MyBaseView(Ethnic, db.session, category="Thông tin chung", name="Dân tộc"))

from my_app.student import *
from my_app.teacher import *
from my_app.educational_office import *