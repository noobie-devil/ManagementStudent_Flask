from my_app.admin import *

class MyEducationalOfficeIndexView(AdminIndexView):
	def is_visible(self):
		return False

	@expose('/')
	def index(self):
		if not current_user.is_authenticated or current_user.is_edu_office() == False:
			flash('Please log in first...', category='danger')
		# 	# next_url = request.url
		# 	# login_url = '%s?next=%s' % (url_for('login_page'), next_url)
			return redirect(url_for('login_page'))
		
		return redirect(url_for('edu_office_resume.index'))

class MyBaseEduOfficeView(MyBaseView):
	def is_accessible(self):
		return current_user.is_authenticated and current_user.is_edu_office()

	def inaccessible_callback(self, name, **kwargs):
		flash('Yêu cầu truy cập không khả dụng!! Hãy đăng nhập', category='danger')
		return redirect(url_for('login_page'))

class PersonalInfoView_EduOffice(PersonalInfoView):
	def is_accessible(self):
		return current_user.is_edu_office()

	def inaccessible_callback(self, name, **kwargs):
		flash('Yêu cầu truy cập không khả dụng!! Hãy đăng nhập', category='danger')
		return redirect(url_for('login_page'))

class ChangePasswordView_EduOffice(ChangePasswordView):
	@expose('/', methods=['GET','POST'])
	def index(self):
		return super(ChangePasswordView_EduOffice, self).index()
	
class ResumeOnlineView(MyBaseEduOfficeView):
	column_list = ['subject','teacher.user.full_name', 'class_info', 'semester', 'school_year']
	can_create = False
	# column_list.append('hello')
	list_template = 'edu_office/list_resume_online.html'
	@expose('/')
	def index(self):
		confirm_resume = self.session.query(Resume).filter(Resume.status == 0).all()
		fields = self.session.query(ResumeImageFields).join(Role).filter(ResumeImageFields.role_id == Role.id, Role.name == 'Học sinh').all()
		lists = []
		for resume in confirm_resume:
			row = {}
			row['id'] = resume.id
			row['full_name'] = resume.user.full_name
			row['fieldsImage'] = []
			for field in fields:
				f = self.session.query(ResumeImageStorage).filter(ResumeImageStorage.resume_id == resume.id, ResumeImageStorage.field_id == field.id).first()
				row['fieldsImage'].append(f.image_path)
				# row['fieldsImage'] = ({'field_name': f.image_path} for f in self.session.query(ResumeImageStorage).filter(ResumeImageStorage.resume_id=resume.id, ResumeImageStorage.field_id = field.id).first())
			lists.append(row)
		self._template_args['resumes'] = lists
		self._template_args['fields'] = fields
		return super(ResumeOnlineView, self).index_view()

	@expose('/ajax-handler', methods=['POST'])
	def handler_ajax(self):
		data = request.json
		resume_id = None
		action = None
		try:
			resume_id = int(data['resume_id'])
			action = str(data['action'])
		except:
			return Response(
				json.dumps({'msg': 'Data invalid !!!', 'category': 'danger'}),
				status=400,
				mimetype='application/json'
			)
		resume = self.session.query(Resume).get(resume_id)
		if action == "confirm":	
			resume.status = 1
			resume.confirmed_at = datetime.now()
			account_student = self.session.query(Account).filter_by(user_id=resume.user_id).first()
			account_student.active = True
		else:
			resume.status = 2
		try:
			self.session.commit()
			return Response(
				json.dumps({'msg': 'Thao tác thực hiện thành công !!!', 'category': 'success'}),
				status=200,
				mimetype='application/json'
			)
		except Exception as ex:
			self.session.rollback()
			return Response(
				json.dumps({'msg': 'Đã xảy ra lỗi !!!', 'category': 'danger'}),
        		status=500,
        		mimetype='application/json'
			)



educational_office = Admin(app, name='Phòng giáo vụ', index_view=MyEducationalOfficeIndexView(url='/edu-office', endpoint='_edu_office', menu_icon_type="ti", menu_icon_value="ti-home"), base_template='master.html', template_mode='bootstrap4', url='/edu-office', endpoint='_edu_office')

educational_office.add_view(ResumeOnlineView(Resume,db.session, name='Hồ sơ nhập học Online', url='/edu-office/online-resume', endpoint='edu_office_resume'))

educational_office.add_view(PersonalInfoView_EduOffice(MoreInfo, db.session, name="Thông tin cá nhân", url='/edu-office/info', endpoint='edu_office_info', menu_icon_type="ti", menu_icon_value="ti-pencil"))

educational_office.add_view(ClassInfoView(ClassInfo, db.session, name="Danh sách lớp", url='/edu-office/list-class', endpoint='edu_office_list_class'))

educational_office.add_view(MyBaseEduOfficeView(TeachingAssignment, db.session,name="Phân công giảng dạy",url='/edu-office/teaching-assignment', endpoint='edu_office_teaching_assignment', menu_icon_type="ti", menu_icon_value="ti-briefcase"))

educational_office.add_view(MyBaseEduOfficeView(Subject, db.session, name="Quản lý môn học", menu_icon_type="ti", menu_icon_value="ti-book", url='/edu-office/subject', endpoint='edu_office_subject'))

educational_office.add_view(MyBaseEduOfficeView(Semester, db.session, name="Học kỳ", url='/edu-office/semester', endpoint='edu_office_semester', menu_icon_type="ti", menu_icon_value="ti-notepad"))

educational_office.add_view(MyBaseEduOfficeView(SchoolYear, db.session, category='Năm học', name="Chỉnh sửa năm học", menu_icon_type="ti", menu_icon_value="ti-calendar", url='/edu-office/school-year', endpoint='edu_office_school_year'))

educational_office.add_view(MyBaseEduOfficeView(Course, db.session, category='Năm học', name="Chỉnh sửa niên khóa", menu_icon_type="ti", menu_icon_value="ti-calendar", url='/edu-office/course-info', endpoint='edu_office_course_info'))

educational_office.add_view(ChangePasswordView_EduOffice(name="Đổi mật khẩu", url="/edu-office/change-password", endpoint='_changePasswordEduOffice'))
