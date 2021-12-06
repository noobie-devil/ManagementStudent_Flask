from my_app.admin import *


class MyTeacherIndexView(AdminIndexView):

	def is_visible(self):
		return False

	@expose('/')
	def index(self):
		if not current_user.is_authenticated or current_user.is_teacher() == False:
			flash('Please log in first...', category='danger')
			# next_url = request.url
			# login_url = '%s?next=%s' % (url_for('login_page'), next_url)
			return redirect(url_for('login_page'))
		return redirect(url_for('teacher_assignment.index_view'))
		# return super(MyTeacherIndexView,self).index()
	
class MyBaseTeacherView(MyBaseView):
	def is_accessible(self):
		return current_user.is_authenticated and current_user.is_teacher()

	def inaccessible_callback(self, name, **kwargs):
		flash('Yêu cầu truy cập không khả dụng!! Hãy đăng nhập', category='danger')
		return redirect(url_for('login_page'))


class TeachingAssignmentView_Teacher(MyBaseTeacherView):
	column_list = ('subject','teacher.user.full_name', 'class_info', 'semester', 'school_year')

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


class InfoSubjectReport:
	def __init__(self, stt, className, number, passs, percent):
		self.STT = stt
		self.ClassName = className
		self.Number = number
		self.Pass = passs
		self.Percent = percent


class SubjectReportView_Teacher(BaseView):
	@expose('/')
	def index(self):
		allDataSubjectReport = []
		countDataSubjectReport = 0
		subject = ""
		getTeacher = Teacher.query.filter_by(user_id=current_user.user_id).first()
		getSemester = Semester.query.filter_by(active = 1)

		for value_semester in getSemester:
			classTeaching = TeachingAssignment.query.join(ClassInfo).filter(TeachingAssignment.teacher_id == getTeacher.id, TeachingAssignment.semester_id == value_semester.id, TeachingAssignment.class_info_id == ClassInfo.id, ClassInfo.amount_std > 0)
			try:
				subject = classTeaching[0].subject.subject_name
			except:
				pass

			transcript_info_id = []
			sizeClassTeaching = 0
			for item in classTeaching:
				sizeClassTeaching += 1
				transcript_info_id.append(item.id)

			avgStudent = SubjectReportView_Teacher.GetStudentPass(transcript_info_id)
			countDataSubjectReport += 1
			dataSubjectReport = SubjectReportView_Teacher.GetSubjectReport(sizeClassTeaching, avgStudent, classTeaching)
			allDataSubjectReport.append(dataSubjectReport)

		countElementDataSubjectReport = []
		for item in allDataSubjectReport:
			countElementDataSubjectReport.append(len(item))

		self._template_args["getSemester"] = getSemester
		self._template_args["subject"] = subject
		self._template_args["countDataSubjectReport"] = countDataSubjectReport
		self._template_args["countElementDataSubjectReport"] = countElementDataSubjectReport
		self._template_args["allDataSubjectReport"] = allDataSubjectReport
		return self.render('teacher/subject-report.html')

	@staticmethod
	def GetStudentPass(transcript_info_id):
		avgStudent = []
		for item in transcript_info_id:
			listSubjectTranscript = SubjectTranscript.query.filter_by(transcript_info_id=item)
			count = 0
			for value in listSubjectTranscript:
				if value.score_average >= 5:
					count += 1
			avgStudent.append(count)
		return avgStudent

	@staticmethod
	def GetSubjectReport(sizeClassTeaching, avgStudent, classTeaching):
		dataSubjectReport = []
		stt = 0
		for index in range(sizeClassTeaching):
			stt += 1
			percent = round((avgStudent[index] / classTeaching[index].class_info.amount_std) * 100, 2)
			infoSubjectReport = InfoSubjectReport(stt, classTeaching[index].class_info.in_class.class_name,
												  classTeaching[index].class_info.amount_std, avgStudent[index],
												  percent)
			dataSubjectReport.append(infoSubjectReport)
		return dataSubjectReport

class InfoStudentReport:
	def __init__(self, id, name, avg, rank):
		self.Id = id
		self.FullName = name
		self.Avg = avg
		self.Rank = rank

class FinalSemesterReportView_Teacher(BaseView):
	def is_visible(self):
		return self.check_main_teacher()
		
	def check_main_teacher(self):
		teacher_id = db.session.query(Teacher).filter_by(user_id = current_user.user.id).first().id
		count = db.session.query(ClassInfo).filter(ClassInfo.teacher_id == teacher_id).count()
		if count > 0:
			return True
		return False

	def is_accessible(self):
		return current_user.is_authenticated and current_user.is_teacher() and self.check_main_teacher()

	

	@expose('/')
	def index(self):
		subjectTranscript = SubjectTranscript.query.all()
		getTeacher = Teacher.query.filter_by(user_id=current_user.user_id).first()
		classTeaching = TeachingAssignment.query.filter_by(teacher_id=getTeacher.id)

		class_info_id = []
		for i in classTeaching:
			if i.class_info.teacher_id == getTeacher.id:
				class_info_id.append(i.class_info.in_class.id)

		getAllStudentInClass = StudentInClass.query.filter_by(class_info_id=class_info_id[0])
		allInfoStudentReport = []
		allScoreAvg = []
		for idStudent in getAllStudentInClass:
			id = idStudent.student.id
			count = 0
			allScore = 0
			for value in subjectTranscript:
				if value.student_id == id:
					if value.score_average is None:
						pass
					else:
						count += 1
						allScore += value.score_average
			fullName = idStudent.student.user.full_name
			avg = allScore / count
			rank = ""
			if avg >= 8:
				rank = "Giỏi"
			elif 6.5 <= avg < 8:
				rank = "Khá"
			elif 4 <= avg < 6.5:
				rank = "Trung bình"
			else:
				rank = "Yếu"
			infoStudentReport = InfoStudentReport(idStudent, fullName, round(avg,2), rank)
			allInfoStudentReport.append(infoStudentReport)

		self._template_args["allInfoStudentReport"] = allInfoStudentReport
		return self.render('teacher/final_semester_report.html')

teacher = Admin(app, name='Teacher', index_view=MyTeacherIndexView(url='/teacher', endpoint='_teacher', menu_icon_type="ti", menu_icon_value="ti-home"), base_template='master.html', template_mode='bootstrap4', url='/teacher', endpoint='_teacher')
teacher.add_view(TeachingAssignmentView_Teacher(TeachingAssignment, db.session, name='Danh sách lớp giảng dạy', url='/teacher/list-class',endpoint='teacher_assignment', menu_icon_type="ti", menu_icon_value="ti-briefcase"))
teacher.add_view(PersonalInfoView_Teacher(MoreInfo, db.session, name="Thông tin cá nhân", url='/teacher/info', endpoint='teacher_info', menu_icon_type="ti", menu_icon_value="ti-pencil"))
teacher.add_view(StudentInClassView_Teacher(StudentInClass, db.session, name='Danh sách học sinh', url='/teacher/list-class', endpoint='class_details'))
teacher.add_view(SubjectTranscriptView_Teacher(SubjectTranscript, db.session, name='Nhập điểm', url='/teacher/list-class', endpoint='score'))
teacher.add_view(ChangePasswordView_Teacher(name="Đổi mật khẩu", url="/teacher/change-password", endpoint='_changePasswordTeacher'))
teacher.add_view(SubjectReportView_Teacher(name='Báo cáo tổng kết môn', url='/teacher/subject-report', endpoint='subject_report'))
teacher.add_view(FinalSemesterReportView_Teacher(name='Báo cáo tổng kết học kỳ', url='/teacher/final-semester-report', endpoint='final_semester_report'))

