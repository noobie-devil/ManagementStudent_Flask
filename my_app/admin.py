from my_app import db,app
from my_app.models import *
from flask import Flask, render_template, redirect, url_for, flash, request, json
from flask_admin import Admin
from my_app import admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView
from flask_login import login_user, logout_user, login_required, current_user
from flask_admin import AdminIndexView, expose, BaseView
from flask_admin.model.fields import InlineModelFormField, InlineFormField, InlineFieldList
from wtforms.utils import unset_value
from wtforms import form,fields
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from flask_wtf import FlaskForm
from my_app.forms import *
from flask_admin.helpers import (get_form_data, validate_form_on_submit, get_redirect_target, flash_errors)
from flask_admin.model.helpers import get_mdict_item_or_list
from flask_admin.contrib.sqla.filters import BaseSQLAFilter, FilterEqual, ChoiceTypeEqualFilter
from flask_admin.model.template import EndpointLinkRowAction
from datetime import datetime
from sqlalchemy import func
from flask_admin.model.template import TemplateLinkRowAction


class MyAdminIndexView(AdminIndexView):
	@expose('/')
	def index(self):
		# if not current_user.is_authenticated or current_user.is_admin == False:
		# 	flash('Please log in first...', category='danger')
		# 	# next_url = request.url
		# 	# login_url = '%s?next=%s' % (url_for('login_page'), next_url)
		# 	return redirect(url_for('login_page'))
		return super(MyAdminIndexView,self).index()
		

class MyStudentIndexView(AdminIndexView):
	@expose('/')
	def index(self):
		if not current_user.is_authenticated or current_user.is_admin == False:
			flash('Please log in first...', category='danger')
			# next_url = request.url
			# login_url = '%s?next=%s' % (url_for('login_page'), next_url)
			return redirect(url_for('login_page'))
		return super(MyStudentIndexView,self).index()
		
class MyTeacherIndexView(AdminIndexView):
	@expose('/')
	def index(self):
		if not current_user.is_authenticated or current_user.is_teacher == False:
			flash('Please log in first...', category='danger')
			# next_url = request.url
			# login_url = '%s?next=%s' % (url_for('login_page'), next_url)
			return redirect(url_for('login_page'))
		return super(MyTeacherIndexView,self).index()
		
	

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


class MyBaseView(ModelView):

	# def is_accessible(self):
	# 	return current_user.is_authenticated

	# def inaccessible_callback(self, name, **kwargs):
	# 	flash('Yêu cầu truy cập không khả dụng!! Hãy đăng nhập', category='danger')
	# 	return redirect(url_for('login_page'))

	form_excluded_columns = ('created_at','modified_at', 'teachingAssignment', 'schoolYear', 'detailsTranscript', 'class')

	list_template = 'admin/list.html'
	column_labels = {
		'user.image': 'Hình ảnh',
		'teacher_code': 'Mã GV',
		'student_code': 'Mã HS',
		'subject': 'Môn  phụ trách',
		'classInfo': 'Lớp',
		'semester': 'Học kỳ',
		'user.full_name': 'Họ và tên',
		'user.gender': 'Giới tính',
		'user.role': 'Role',
		'user.birthdate': 'Ngày sinh',
		'user.ethnic': 'Dân tộc',
		'user.nationality': 'Quốc tịch',
		'user.permanent_address': 'Địa chỉ thường trú',
		'user.home_town': 'Quê quán',
		'class_name': 'Lớp',
		'created_at': 'Ngày tạo',
		'semester_name': 'Tên học kỳ',
		'year': 'Năm học',
		'gender_name': 'Giới tính',
		'nationality_name': 'Quốc tịch',
		'ethnic_name': 'Dân tộc',
		'score_name': 'Cột điểm',
		'multiplier': 'Hệ số',
		'course.course_name': 'Khóa',
		'course.time': 'Niên khóa',
		'course': 'Khóa',
		'course_name': 'Khóa',
		'start_year': 'Năm bắt đầu',
		'end_year': 'Năm kết thúc',
		'grade_name': 'Khối',
		'grade': 'Khối',
		'subject_name': 'Môn học',
		'letter_point': 'Điểm chữ',
		'in_class.class_name': 'Lớp',
		'school_year': 'Năm học',
		'amount_std': 'Sĩ số',
		'teacher.user.full_name': 'Giáo Viên',
		'semester.semester_name': 'Học kỳ',
		'student.user.full_name': 'Họ tên',
		'classInfo.school_year' : 'Năm học',
		'student' : 'Mã HS'

	}
	form_widget_args = {
        'student_code': {
            'readonly': True
        },
        'teacher_code': {
            'readonly': True
        },
    }


class CourseView(MyBaseView):
	form_excluded_columns = ('time','student')

	def on_model_change(self, form, Course, is_created):
		Course.time = form.start_year.data + '-' + form.end_year.data

class UserView(MyBaseView):
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
		if is_created and form.user_id:
			model.user_id = form.user_id

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
			auto_create_account.role_id = model.user.role_id
			try:
				self.session.add(auto_create_account)
				self.session.commit()
			except Exception as ex:
				self.session.rollback()

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
			form.teacher_code.data = 'GV' + '{:0>5}'.format(1)
		else:
			if max_id != False:
				form.teacher_code.data = 'GV' + '{:0>5}'.format(max_id+1)
		
		return form

	
	def create_model(self,form):
		user_to_create = create_user(form,'Giáo viên')
		db.session.add(user_to_create)
		db.session.commit()
		form.user_id = user_to_create.id
		return super(TeacherView,self).create_model(form)

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
    column_list = ('id','username', 'password_hash', 'active', 'created_at' )
    column_labels = dict(password_hash='Password Hashed', created_at='Ngày tạo')
    form_columns = ('user','username','password', 'role', 'active')
    form_extra_fields = {
        'password': fields.PasswordField(label='Password:',validators=[Length(min=8, max=60), DataRequired()])
    }
    def on_model_change(self, form, Account, is_created):
        if form.password.data:
        	Account.password = form.password.data

class PersonalInfoView(MyBaseView):

	# def edit_form(self):
	# 	form = UpdateInfoForm()
	# 	return form

	# def update_model(self, form, model):
	# 	info_update = self.session.query(MoreInfo).get(current_user.user_id)
	# 	info_update.email= form.u_email.data
	# 	info_update.phone= form.u_phone.data
	# 	info_update.current_residence= form.u_residence.data
	# 	info_update.note= form.note.data
	# 	db.session.commit()
	# 	return redirect(url_for('admin_info.info_view'))

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

			return redirect(url_for('admin_info.info_view'))
		more_info = MoreInfo.query.filter_by(user_id=current_user.user_id)
		return self.render('admin/edit_info.html', update_info_form=update_info_form, more_info=more_info)

	def render(self, template, **kwargs):
		more_info = MoreInfo.query.get(current_user.user_id)	
		if more_info is not None:
			kwargs['more_info'] = more_info
		return super(PersonalInfoView, self).render(template, **kwargs)

class PersonalInfoView_Student(PersonalInfoView):
	list_template = 'student/info.html'
	@expose('/')
	def info_view(self):
		return super(PersonalInfoView_Student,self).list_view()

	edit_template = 'student/edit_info.html'

	@expose('/edit', methods=['GET','POST'])
	def edit_view(self):
		update_info_form = UpdateInfoForm()
		if request.method == "POST":
			more_info = MoreInfo.query.filter_by(user_id=current_user.user_id).first()
			if more_info is not None:
				more_info.email = update_info_form.u_email.data
				more_info.phone = update_info_form.u_phone.data
				more_info.current_residence = update_info_form.u_residence.data
				more_info.note = update_info_form.note.data
			else: 
				more_info = MoreInfo(user_id=current_user.user_id,email=update_info_form.u_email.data,phone=update_info_form.u_phone.data,current_residence=update_info_form.u_residence.data,note=update_info_form.note.data,modified_at=datetime.now())
				db.session.add(more_info)
			student_to_update = Student.query.filter_by(user_id=current_user.user_id).first()
			family_info = FamilyInfo.query.filter_by(student_id=student_to_update.id).first()
			if family_info is not None:
				family_info.full_name = update_info_form.contact_name.data
				family_info.phone = update_info_form.contact_phone.data
				family_info.current_residence = update_info_form.contact_residence.data
			family_info = FamilyInfo(student_id=student_to_update.id, full_name=update_info_form.contact_name.data, phone=update_info_form.contact_phone.data, current_residence=update_info_form.contact_residence.data, modified_at=datetime.now())
			db.session.add(family_info)

			db.session.commit()
			return redirect(url_for('student_info.info_view'))
		more_info = MoreInfo.query.filter_by(user_id=current_user.user_id)
		return self.render('student/edit_info.html', update_info_form=update_info_form, more_info=more_info)

	def render(self, template, **kwargs):
		student = Student.query.filter_by(user_id=current_user.user_id).first()
		family_info = FamilyInfo.query.filter_by(student_id=student.id).first()
		kwargs['student'] = student
		kwargs['family_info'] = family_info
		return super(PersonalInfoView_Student, self).render(template, **kwargs)
# class PersonalInfoView(BaseView):
# 	@expose('/')
# 	def index(self):
# 		if not current_user.is_authenticated:
# 			flash('Please log in first...', category='danger')
# 			# next_url = request.url
# 			# login_url = '%s?next=%s' % (url_for('login_page'), next_url)
# 			return redirect(url_for('login_page'))
# 		if current_user.is_admin():	
# 			return self.render('admin/info.html')
# 		if current_user.is_student():
# 			return self.render('student/info.html')

# 	def is_accessible(self):
# 		return current_user.is_authenticated

# 	def inaccessible_callback(self, name, **kwargs):
# 		flash('Yêu cầu truy cập không khả dụng!! Hãy đăng nhập', category='danger')
# 		return redirect(url_for('login_page'))	

# 	@expose('/edit', methods=['GET','POST'])
# 	def edit(self):
# 		update_info_form = UpdateInfoForm()
# 		if request.method == "POST":
# 		# if update_info_form.validate_on_submit():
# 			more_info = MoreInfo.query.filter_by(user_id=current_user.user_id).first()
# 			if more_info is not None:
# 				more_info.email = update_info_form.u_email.data
# 				more_info.phone = update_info_form.u_phone.data
# 				more_info.current_residence = update_info_form.u_residence.data
# 				more_info.note = update_info_form.note.data
# 			else: 
# 				more_info = MoreInfo(user_id=current_user.user_id,email=update_info_form.u_email.data,phone=update_info_form.u_phone.data,current_residence=update_info_form.u_residence.data,note=update_info_form.note.data,modified_at=datetime.now())
# 				db.session.add(more_info)
			
# 			if current_user.role.name == "Học sinh":
# 				student_to_update = Student.query.filter_by(user_id=current_user.user_id).first()
# 				family_info = FamilyInfo(student_id=student_to_update.id, full_name=update_info_form.contact_name.data, phone=update_info_form.contact_phone.data, current_residence=update_info_form.contact_residence.data, modified_at=datetime.now())
# 				db.session.add(family_info)
# 			db.session.commit()

# 			return redirect(url_for('admin_info.index'))
# 		more_info = MoreInfo.query.filter_by(user_id=current_user.user_id)
# 		return self.render('admin/edit_info.html', update_info_form=update_info_form, more_info=more_info)

# 	def render(self, template, **kwargs):
# 		more_info = MoreInfo.query.get(current_user.user_id)
# 		if current_user.role.name == "Học Sinh":
# 			student = Student.query.filter_by(user_id=current_user.user_id).first()
# 			family_info = FamilyInfo.query.filter_by(student_id=student.id).first()
# 			if family_info is not None:
# 				kwargs['family_info'] = family_info
# 			kwargs['student'] = student	
# 		if more_info is not None:
# 			kwargs['more_info'] = more_info

# 		return super(PersonalInfoView, self).render(template, **kwargs)

class TeachingAssignmentView(MyBaseView):
	column_list = ('subject','teacher.user.full_name', 'classInfo', 'semester', 'school_year')
	# column_extra_row_actions = [
	# 	EndpointLinkRowAction('ti ti-pencil', '.function'),
	# ]
	column_extra_row_actions = [# Add a new action button
		TemplateLinkRowAction("custom_row_actions.copy_row", "Show List Students"),
	]
	can_edit = False
	can_delete = False

	@expose('/function')
	def copy_view(self):
		pass
	def get_query(self):
		if current_user.is_teacher:
			teacher_id = Teacher.query.filter_by(user_id=current_user.user_id).first().id
			return self.session.query(self.model).filter(self.model.teacher_id == teacher_id)
		else:
			return super(TeachingAssignmentView,self).get_query(self)

	list_template = 'teacher/list_class.html'
	@expose('/')
	def info_view(self):
		return super(TeachingAssignmentView,self).list_view()


class StudentInClassView_Teacher(MyBaseView):
	column_list = ('student','student.user.full_name', 'classInfo', 'classInfo.school_year')
	can_delete = False
	def get_query(self):
		cid = False if request.args.get('cid') is None else request.args.get('cid')
		if cid != False:
			return self.session.query(self.model).filter(self.model.class_info_id == int(cid))
		else:
			return self.session.query(self.model)

	list_template='teacher/list_students.html'
	@expose('/class')
	def list_students(self):
		self._template_args['teaching_id'] = request.args.get('teaching-id')
		self._template_args['cid'] = request.args.get('cid')		
		return super(StudentInClassView_Teacher,self).index_view()


class SubjectTranscriptView_Teacher(MyBaseView):
	column_list = ('student','transcript_details')
	can_delete = False
	list_template = 'teacher/edit_score.html'


	def get_query(self):
		action = False if request.args.get('action') is None else request.args.get('action')
		teaching_id = False if request.args.get('teaching-id') is None else request.args.get('teaching-id')
		if action != False and action == 'edit':
			return self.session.query(self.model).filter(self.model.transcript_info_id == int(teaching_id))
		else:
			return self.session.query(self.model)

	def get_field(self,field):
		if field.fieldtype == "float":
			return fields.FloatField(field.label)

	@expose('/class/score')
	def score_view(self):
		class DynamicForm(FlaskForm):pass

		# dform = self.models.Form.objects.get(name='scoreType')
		score_type = [(type.id, type.score_name) for type in ScoreType.query.all()]

		for item in score_type:
			setattr(DynamicForm, str(item[0]), fields.FloatField(item[1]))
		form = DynamicForm()
		# score_type = [{"score.label": type.score_name} for type in ScoreType.query.all()]
		# form = TranscriptForm(transcripts=score_type)
		action = False if request.args.get('action') is None else request.args.get('action')
		if action != False and action == 'edit':
			self._template_args['form'] = form
			return super(SubjectTranscriptView_Teacher,self).index_view()		

	# def render(self, template, **kwargs):
	# 	if template == 'teacher/edit_score.html':
	# 		kwargs['summary_data'] = [
	# 			{'title': 'Page Total', 'name': None, 'cost': '1000'},
	# 			{'title': 'Grand Total', 'name': None, 'cost': '2000'},
	# 		]
	# 	return super(SubjectTranscriptView_Teacher, self).render(template, **kwargs)



admin = Admin(app, name='UTE', index_view=MyAdminIndexView(), base_template='master.html', template_mode='bootstrap4')

admin.add_view(PersonalInfoView(MoreInfo, db.session, name="Thông tin cá nhân", url='/admin/info', endpoint='admin_info'))
admin.add_view(AccountView(Account, db.session, category="Quản lý tài khoản", name="Tài khoản"))
admin.add_view(MyBaseView(User, db.session, category="Quản lý tài khoản", name="Người dùng"))
admin.add_view(MyBaseView(Role, db.session, category="Quản lý tài khoản", name="Thông tin quyền"))
admin.add_view(MyBaseView(MoreInfo, db.session, category="Quản lý tài khoản", name="Thông tin mở rộng"))

admin.add_view(StudentView(Student, db.session, category="Quản lý học sinh", name="Chỉnh sửa"))
# admin.add_view(MyBaseView(FamilyMember, db.session, category="Quản lý học sinh",name="Thành phần gia đình"))


admin.add_view(TeacherView(Teacher, db.session, name="Giáo viên", menu_icon_type="ti", menu_icon_value="ti-user"))

admin.add_view(AdminView(Administrator, db.session, name="Quản trị viên", menu_icon_type="ti", menu_icon_value="ti-user"))

admin.add_view(EducationalOfficeView(EducationalOffice, db.session, name="Phòng giáo vụ", menu_icon_type="ti", menu_icon_value="ti-user"))

admin.add_view(MyBaseView(Class, db.session, category="Quản lý lớp học", name="Thông tin lớp học"))
admin.add_view(ClassInfoView(ClassInfo, db.session, category="Quản lý lớp học", name="Danh sách lớp học trong năm"))
admin.add_view(MyBaseView(TeachingAssignment, db.session, category="Quản lý lớp học",name="Phân công giảng dạy"))

admin.add_view(MyBaseView(Subject, db.session, name="Quản lý môn học", menu_icon_type="ti", menu_icon_value="ti-book"))

admin.add_view(MyBaseView(ScoreType, db.session, category="Quản lý điểm", name="Thông tin bảng điểm"))
admin.add_view(MyBaseView(SubjectTranscript, db.session, category="Quản lý điểm", name="Điểm theo môn học"))
admin.add_view(MyBaseView(StudentInClass, db.session, category="Quản lý điểm", name="Chỉnh sửa điểm học sinh"))

admin.add_view(MyBaseView(Semester, db.session, name="Học kỳ"))

admin.add_view(MyBaseView(SchoolYear, db.session, category='Năm học', name="Chỉnh sửa năm học", menu_icon_type="ti", menu_icon_value="ti-calendar"))
admin.add_view(CourseView(Course, db.session, category='Năm học', name="Chỉnh sửa niên khóa", menu_icon_type="ti", menu_icon_value="ti-calendar"))

admin.add_view(MyBaseView(Grade,db.session, category="Thông tin chung", name="Khối"))
admin.add_view(MyBaseView(Gender, db.session, category="Thông tin chung", name="Giới tính") )
admin.add_view(MyBaseView(Nationality, db.session, category="Thông tin chung", name="Quốc tịch"))
admin.add_view(MyBaseView(Ethnic, db.session, category="Thông tin chung", name="Dân tộc"))

student = Admin(app, name='Student', index_view=MyStudentIndexView(url='/student', endpoint='_student'), base_template='master.html', template_mode='bootstrap4', url='/student', endpoint='_student')
student.add_view(PersonalInfoView_Student(MoreInfo,db.session, name='Thông tin cá nhân', url='/student/info', endpoint='student_info'))

teacher = Admin(app, name='Teacher', index_view=MyTeacherIndexView(url='/teacher', endpoint='_teacher'), base_template='master.html', template_mode='bootstrap4', url='/teacher', endpoint='_teacher')
teacher.add_view(TeachingAssignmentView(TeachingAssignment, db.session, name='Danh sách lớp giảng dạy', url='/teacher/list-class',endpoint='teacher_assignment'))
teacher.add_view(StudentInClassView_Teacher(StudentInClass, db.session, name='Danh sách học sinh', url='/teacher/list-class', endpoint='class_details'))
teacher.add_view(SubjectTranscriptView_Teacher(SubjectTranscript, db.session, name='Nhập điểm', url='/teacher/list-class', endpoint='score'))