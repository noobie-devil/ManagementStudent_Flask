from my_app.admin import *

class MyTeacherIndexView(AdminIndexView):
	@expose('/')
	def index(self):
		if not current_user.is_authenticated or current_user.is_teacher() == False:
			flash('Please log in first...', category='danger')
			# next_url = request.url
			# login_url = '%s?next=%s' % (url_for('login_page'), next_url)
			return redirect(url_for('login_page'))
		users = User.query.filter_by(id=current_user.user_id).first()
		self._template_args["info"] = users
		return super(MyTeacherIndexView,self).index()
	
class MyBaseTeacherView(MyBaseView):
	def is_accessible(self):
		return current_user.is_teacher()

	def inaccessible_callback(self, name, **kwargs):
		flash('Yêu cầu truy cập không khả dụng!! Hãy đăng nhập', category='danger')
		return redirect(url_for('login_page'))

class TeachingAssignmentView_Teacher(MyBaseTeacherView):
	column_list = ('subject','teacher.user.full_name', 'class_info', 'semester', 'school_year')
	# column_extra_row_actions = [
	# 	EndpointLinkRowAction('ti ti-pencil', '.function'),
	# ]
	column_extra_row_actions = [# Add a new action button
		TemplateLinkRowAction("custom_row_actions.copy_row", "Show List Students"),
	]
	can_edit = False
	can_delete = False
	can_create = False

# 	<!-- <form class="icon" method="POST" action="{{ get_url('.copy_view') }}">
#   <input type="hidden" name="row_id" value="{{ get_pk_value(row) }}"/>
#   <button type="submit" title="{{ _gettext('Copy record') }}">
#     <span class="ti ti-pencil"></span>
#   </button>
# </form> -->

	def get_query(self):
		teacher_id = Teacher.query.filter_by(user_id=current_user.user_id).first().id
		return self.session.query(self.model).join(Semester).join(SchoolYear).filter(self.model.teacher_id == teacher_id, Semester.active == True, self.model.semester_id == Semester.id, self.model.school_year_id == SchoolYear.id, SchoolYear.active == True)
	

	def get_count_query(self):
		teacher_id = Teacher.query.filter_by(user_id=current_user.user_id).first().id
		return self.session.query(func.count('*')).select_from(self.model).join(Semester).join(SchoolYear).filter(self.model.teacher_id == teacher_id, Semester.active == True, self.model.semester_id == Semester.id, self.model.school_year_id == SchoolYear.id, SchoolYear.active == True)

	list_template = 'teacher/list_class.html'
	@expose('/')
	def info_view(self):
		return super(TeachingAssignmentView,self).list_view()


class StudentInClassView_Teacher(MyBaseTeacherView):
	def is_visible(self):
		return False
		

	column_list = ('student','student.user.full_name', 'classInfo', 'classInfo.school_year')
	can_delete = False
	can_create = False
	can_edit = False
	def get_query(self):
		cid = False if request.args.get('cid') is None else request.args.get('cid')
		if cid != False:
			return self.session.query(self.model).filter(self.model.class_info_id == int(cid))
		else:
			return self.session.query(self.model)

	def get_count_query(self):
		return self.session.query(func.count('*')).select_from(self.model).filter(self.model.class_info_id == int(request.args.get('cid')))

	list_template='teacher/list_students.html'
	@expose('/class')
	def list_students(self):
		self._template_args['teaching_id'] = request.args.get('teaching-id')
		self._template_args['cid'] = request.args.get('cid')		
		return super(StudentInClassView_Teacher,self).index_view()


class SubjectTranscriptView_Teacher(MyBaseTeacherView):
	def is_visible(self):
		return False

	column_list = ('student','transcript_details')
	can_delete = False
	list_template = 'teacher/edit_score.html'
	can_create = False

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


	@expose('/class/score/ajax-update', methods=['POST'])
	def update_score_ajax(self):
		editable = self.check_editable()
		if editable != 1:
			return Response(
				json.dumps({"msg": "Yêu cầu không khả dụng", "flash_msg": "Yêu cầu không khả dụng!!! Đang trong thời gian không cho phép nhập điểm."}),
				status=400,
				mimetype='application/json'
			)

		subject_transcript_id = request.form['pk']
		score_type_id = request.form['score']
		value = request.form['value']
		if subject_transcript_id and score_type_id:
			if value != '':
				try:
					value = round(float(value), 2)
				except:
					return Response(
						json.dumps({"msg": "data invalid"}),
						status=400,
						mimetype='application/json'
					)

				if value < 0 or value > 10:
					return Response(
						json.dumps({"msg": "Chỉ nhập vào số từ 0 đến 10"}),
						status=400,
						mimetype='application/json'
					)
				else:
					return self.update_score(value, subject_transcript_id, score_type_id)
			else:
				value = None
				return self.update_score(value, subject_transcript_id, score_type_id)

	def update_score(self, value, subject_transcript_id, score_type_id):
		update = db.session.query(DetailsTranscript).filter_by(transcript_id = subject_transcript_id, score_type_id= score_type_id).first()
		if update != None:
			update.score = value
			update.modified_at = datetime.now()
			self.session.commit()
		else:
			update = DetailsTranscript()
			update.score_type_id = score_type_id
			update.transcript_id = subject_transcript_id
			update.score = value
			self.session.add(update)
			self.session.commit()

		get_all_score = db.session.query(DetailsTranscript).filter_by(transcript_id=subject_transcript_id).all()
		_sum = 0
		_mul = 0
		for i in get_all_score:
			_sum += i.score * i.score_type.multiplier
			_mul += i.score_type.multiplier
		sub = self.session.query(SubjectTranscript).filter_by(id=subject_transcript_id).first()
		sub.score_average = round(float(_sum/_mul),2)
		self.session.commit()
		return Response(
			json.dumps({"newValue" : str(update.score)}),
			status=200,
			mimetype='application/json'
		)

	
	def check_editable(self):
		editable = InputScoreTime.query.filter(InputScoreTime.start_date <= datetime.now(), InputScoreTime.end_date >= datetime.now()).first()
		if editable != None:
			if editable.status == True:
				editable = 1
			else:
				editable = 0
		else:
			editable = 0
		return editable

	@expose('/class/score')
	def score_view(self):
		editable = self.check_editable()
		teaching_assignment = TeachingAssignment.query.get(int(request.args.get('teaching-id')))
		class_info = teaching_assignment.class_info
		list_students = [(std.student.student_code, std.student.user.full_name) for std in class_info.student_In_Class]
		students = db.session.query(SubjectTranscript).filter_by(transcript_info_id=int(request.args.get('teaching-id'))).all()
		lists = []
		score = self.session.query(ScoreType).all()

		for row in students:
			dictret = dict(row.__dict__)
			dictret.pop('_sa_instance_state', None)
			dictret['score'] = [{'id': s.id, 'score_name': s.score_name} for s in score]
			for s in dictret['score']:
				check = db.session.query(DetailsTranscript).filter_by(transcript_id = dictret['id'], score_type_id = s['id']).first()
				if check != None:
					s['score_value'] = check.score
			lists.append(dictret)

		score_type = [{"score.label": type.score_name} for type in ScoreType.query.all()]


		action = False if request.args.get('action') is None else request.args.get('action')
		if action != False and action == 'edit':
			self._template_args['class_info_id'] = class_info.id
			self._template_args['teaching_id'] = request.args.get('teaching-id')
			self._template_args['students'] = list_students
			self._template_args['teaching_assignment'] = teaching_assignment
			self._template_args['score'] = score
			self._template_args['lists'] = lists
			session['editable'] = editable
			return super(SubjectTranscriptView_Teacher,self).index_view()		

class PersonalInfoView_Teacher(PersonalInfoView):
	def is_accessible(self):
		return current_user.is_teacher()

	def inaccessible_callback(self, name, **kwargs):
		flash('Yêu cầu truy cập không khả dụng!! Hãy đăng nhập', category='danger')
		return redirect(url_for('login_page'))

	def render(self, template, **kwargs):
		teacher = Teacher.query.filter_by(user_id=current_user.user_id).first()
		kwargs['teacher'] = teacher
		return super(PersonalInfoView_Teacher, self).render(template, **kwargs)

class ChangePasswordView_Teacher(ChangePasswordView):
	@expose('/', methods=['GET','POST'])
	def index(self):
		return super(ChangePasswordView_Teacher, self).index()

teacher = Admin(app, name='Teacher', index_view=MyTeacherIndexView(url='/teacher', endpoint='_teacher'), base_template='master.html', template_mode='bootstrap4', url='/teacher', endpoint='_teacher')
teacher.add_view(PersonalInfoView_Teacher(MoreInfo, db.session, name="Thông tin cá nhân", url='/teacher/info', endpoint='teacher_info', menu_icon_type="ti", menu_icon_value="ti-pencil"))
teacher.add_view(TeachingAssignmentView_Teacher(TeachingAssignment, db.session, name='Danh sách lớp giảng dạy', url='/teacher/list-class',endpoint='teacher_assignment'))
teacher.add_view(StudentInClassView_Teacher(StudentInClass, db.session, name='Danh sách học sinh', url='/teacher/list-class', endpoint='class_details'))
teacher.add_view(SubjectTranscriptView_Teacher(SubjectTranscript, db.session, name='Nhập điểm', url='/teacher/list-class', endpoint='score'))
teacher.add_view(ChangePasswordView_Teacher(name="Đổi mật khẩu", url="/teacher/change-password", endpoint='_changePasswordTeacher'))
