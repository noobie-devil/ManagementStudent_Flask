from my_app.admin import *

class MyTeacherIndexView(AdminIndexView):
	@expose('/')
	def index(self):
		if not current_user.is_authenticated or current_user.is_teacher == False:
			flash('Please log in first...', category='danger')
			# next_url = request.url
			# login_url = '%s?next=%s' % (url_for('login_page'), next_url)
			return redirect(url_for('login_page'))
		return super(MyTeacherIndexView,self).index()
		
class TeachingAssignmentView_Teacher(MyBaseView):
	column_list = ('subject','teacher.user.full_name', 'classInfo', 'semester', 'school_year')
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
		if current_user.is_teacher:
			teacher_id = Teacher.query.filter_by(user_id=current_user.user_id).first().id
			return self.session.query(self.model).filter(self.model.teacher_id == teacher_id)
		
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
		class_info = TeachingAssignment.query.get(int(request.args.get('teaching-id'))).class_info
		list_students = [(std.student.student_code, std.student.user.full_name) for std in class_info.student_In_Class]
		# session.query(Table1.field1, Table1.field2)\
		# .outerjoin(Table2)
		# .outerjoin(Table2, Table1.id == Table2.table_id)\ # use if you do not have relationship defined
		# .filter(Table2.tbl2_id == None)
		score = self.session.query(ScoreType).all()
		# for item in score_type:
		# 	setattr(DynamicForm, str(item[0]), fields.FloatField(item[1]))

		form = TranscriptForm(transcripts=score_type)

		# form = DynamicForm()
		score_type = [{"score.label": type.score_name} for type in ScoreType.query.all()]
		form = TranscriptForm(transcripts=score_type)
		action = False if request.args.get('action') is None else request.args.get('action')
		if action != False and action == 'edit':
			self._template_args['students'] = list_students
			self._template_args['form'] = form
			self._template_args['score'] = score
			return super(SubjectTranscriptView_Teacher,self).index_view()		

	# def render(self, template, **kwargs):
	# 	if template == 'teacher/edit_score.html':
	# 		kwargs['summary_data'] = [
	# 			{'title': 'Page Total', 'name': None, 'cost': '1000'},
	# 			{'title': 'Grand Total', 'name': None, 'cost': '2000'},
	# 		]
	# 	return super(SubjectTranscriptView_Teacher, self).render(template, **kwargs)


teacher = Admin(app, name='Teacher', index_view=MyTeacherIndexView(url='/teacher', endpoint='_teacher'), base_template='master.html', template_mode='bootstrap4', url='/teacher', endpoint='_teacher')
teacher.add_view(TeachingAssignmentView_Teacher(TeachingAssignment, db.session, name='Danh sách lớp giảng dạy', url='/teacher/list-class',endpoint='teacher_assignment'))
teacher.add_view(StudentInClassView_Teacher(StudentInClass, db.session, name='Danh sách học sinh', url='/teacher/list-class', endpoint='class_details'))
teacher.add_view(SubjectTranscriptView_Teacher(SubjectTranscript, db.session, name='Nhập điểm', url='/teacher/list-class', endpoint='score'))