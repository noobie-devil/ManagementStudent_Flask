from my_app import db, login_manager
from datetime import datetime
from my_app import bcrypt
from flask_login.mixins import *
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
	flash("You must be logged in.")
	return redirect(url_for('login_page'))

class Subject(db.Model):
	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	subject_name = db.Column(db.String(length=60), nullable=False, unique=True)
	active = db.Column(db.Boolean(), nullable = False, default=True)
	letter_point = db.Column(db.Boolean(), nullable=False, default=False)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
	def __str__(self):
		return self.subject_name

class Ethnic(db.Model):
	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	ethnic_name = db.Column(db.String(length=50), nullable=False, unique=True)
	def __str__(self):
		return self.ethnic_name

class Gender(db.Model):
	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	gender_name = db.Column(db.String(length=10), nullable=False, unique=True)
	def __str__(self):
		return self.gender_name

class Nationality(db.Model):
	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	nationality_name = db.Column(db.String(length=50), nullable=False, unique=True)
	def __str__(self):
		return self.nationality_name

class Semester(db.Model):
	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	semester_name =  db.Column(db.String(length=50), nullable=False, unique=True)
	display_name = db.Column(db.String(length=50), nullable=False, unique=True)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
	active = db.Column(db.Boolean(), nullable=False, default=False)
	def __str__(self):
		return self.semester_name

class SchoolYear(db.Model):
	__tablename__ = 'schoolyear'
	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	year = db.Column(db.String(length=50), nullable=False, unique=True)
	active = db.Column(db.Boolean(), default=False)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
	def __str__(self):
		return self.year

class Grade(db.Model):
	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	grade_name = db.Column(db.String(length=20), nullable=False, unique=True)
	def __str__(self):
		return self.grade_name

class Class(db.Model):
	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	class_name = db.Column(db.String(length=50), nullable=False, unique=True)
	grade_id = db.Column(db.Integer(),db.ForeignKey('grade.id'), nullable=False)
	grade = db.relationship('Grade', backref='class', lazy=False)
	active = db.Column(db.Boolean(), default=True)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
	def __str__(self):
		return self.class_name

class FamilyInfo(db.Model):
	__tablename__ = 'familyinfo'
	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	student_id = db.Column(db.Integer(), db.ForeignKey('student.id'), nullable=False)
	full_name = db.Column(db.String(length=50), nullable=True)
	phone = db.Column(db.String(length=20), nullable=False)
	current_residence = db.Column(db.String(length=120), nullable=True)
	modified_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
	def __str__(self):
		return self.full_name

class MoreInfo(db.Model):
	__tablename__ = 'moreinfo'
	user_id = db.Column(db.Integer(), db.ForeignKey('user.id'),primary_key=True)
	email = db.Column(db.String(length=120), nullable=True, unique=True)
	phone = db.Column(db.String(length=20), nullable=True)
	current_residence = db.Column(db.String(length=120), nullable=True)
	note = db.Column(db.Text(), nullable=True)
	modified_at = db.Column(db.DateTime,nullable=False, default=datetime.now())

class Role(db.Model):
	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	name = db.Column(db.String(length=50), nullable=False, unique=True)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

	def __str__(self):
		return self.name

class Course(db.Model):
	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	course_name = db.Column(db.String(length=100), nullable=False)
	time = db.Column(db.String(length=100), nullable=False)
	start_year = db.Column(db.String(length=20), nullable=False, unique=True)
	end_year = db.Column(db.String(length=20), nullable=False, unique=True)
	active = db.Column(db.Boolean(), nullable=False, default=False)
	def __str__(self):
		return self.course_name

class Account(db.Model, UserMixin):
	user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), primary_key=True)
	user = db.relationship('User', backref='account', lazy=False)
	username = db.Column(db.String(length=30), nullable=False, unique=True)
	password_hash = db.Column(db.String(length=60),nullable=False)
	role_id = db.Column(db.Integer(), db.ForeignKey('role.id'), nullable=False)
	role = db.relationship('Role', backref='account', lazy=False)
	active = db.Column(db.Boolean(), nullable=False, default=True)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

	@property
	def password(self):
		return self.password_hash

	@password.setter
	def password(self, plain_text_password):
		self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

	def check_password_correction(self, attempted_password):
		return bcrypt.check_password_hash(self.password_hash, attempted_password)

	def is_admin(self):
		return self.role.name == self.user.role.name == "Admin"

	def is_student(self):
		return self.role.name == self.user.role.name == "Học Sinh"

	def is_teacher(self):
		return self.role.name == self.user.role.name == "Giáo Viên"

	def is_edu_office(self):
		return self.role.name == self.user.role.name == 'Giáo vụ'

	def is_active(self):
		return self.active

	def get_id(self):
		try:
			return text_type(self.user_id)
		except AttributeError:
			raise NotImplementedError('No `id` attribute - override `get_id`')

class User(db.Model):
	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	full_name = db.Column(db.String(length=50), nullable=False)

	gender_id = db.Column(db.Integer(), db.ForeignKey('gender.id'), nullable=False)
	gender = db.relationship('Gender', backref='student', lazy=False)

	birthdate = db.Column(db.Date(), nullable=False)

	ethnic_id = db.Column(db.Integer(), db.ForeignKey('ethnic.id'),nullable=False)
	ethnic = db.relationship('Ethnic', backref='student', lazy=False)

	nationality_id = db.Column(db.Integer(), db.ForeignKey('nationality.id'),nullable=False)
	nationality = db.relationship('Nationality', backref='student', lazy=False)

	permanent_address = db.Column(db.String(length=250), nullable=False)
	home_town = db.Column(db.String(length=50), nullable=False)

	more_info = db.relationship('MoreInfo', backref='user', lazy=False)
	image_id = db.Column(db.String(length=200), nullable=True)
	image = db.Column(db.String(length=200), nullable=True)
	role_id = db.Column(db.Integer(), db.ForeignKey('role.id'), nullable=False)
	role = db.relationship('Role', backref='user', lazy=False)
	# note = db.Column(db.Text(), nullable=True)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

	def __str__(self):
		return self.full_name

class Student(db.Model):
	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	student_code = db.Column(db.String(length=20), nullable=False)
	user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
	user = db.relationship('User', backref='student', lazy=False)
	course_id = db.Column(db.Integer(), db.ForeignKey('course.id'), nullable=False)
	course = db.relationship('Course', backref='student', lazy=False)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
	family_info = db.relationship('FamilyInfo', backref='student', lazy=False)
	def __str__(self):
		return self.student_code

class Teacher(db.Model):
	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	teacher_code = db.Column(db.String(length=20), nullable=False)
	user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
	user = db.relationship('User', backref='teacher', lazy=False)

	subject_id = db.Column(db.Integer(), db.ForeignKey('subject.id'), nullable=True)
	subject = db.relationship('Subject', backref='teacher', lazy=False)

	created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
	def __str__(self):
		return self.teacher_code

class ClassInfo(db.Model):
	__tablename__ = 'classinfo'
	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

	class_id = db.Column(db.Integer(), db.ForeignKey('class.id'), nullable=False)
	in_class = db.relationship('Class', backref='classInfo', lazy=False)

	school_year_id = db.Column(db.Integer(), db.ForeignKey('schoolyear.id'), nullable=False)
	school_year = db.relationship('SchoolYear', backref='classInfo', lazy=False)

	teacher_id = db.Column(db.Integer(), db.ForeignKey('teacher.id'), nullable=True)
	teacher = db.relationship('Teacher', backref='classInfo', lazy=False)

	amount_std = db.Column(db.Integer(), nullable=True)
	student_In_Class = db.relationship('StudentInClass', backref='classInfo', lazy=False)
	def __str__(self):
		# return self.school_year + " - " + self.school_year
		return self.in_class.class_name

class StudentInClass(db.Model):
	__tablename__ = 'studentinclass'
	class_info_id = db.Column(db.Integer(), db.ForeignKey('classinfo.id'), primary_key=True)
	student_id = db.Column(db.Integer(),  db.ForeignKey('student.id'), primary_key=True)
	student = db.relationship('Student', backref='studentInClass', lazy=False)
	def __str__(self):
		return self.student.student_code

class TeachingAssignment(db.Model):
	__tablename__ = "teachingassignment"
	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

	subject_id = db.Column(db.Integer(), db.ForeignKey('subject.id'), nullable=False)
	subject = db.relationship('Subject', backref='teachingAssignment', lazy=False)

	teacher_id = db.Column(db.Integer(), db.ForeignKey('teacher.id'), nullable=False)
	teacher = db.relationship('Teacher', backref='teachingAssignment', lazy=False)

	class_info_id = db.Column(db.Integer(), db.ForeignKey('classinfo.id'), nullable=False)
	class_info = db.relationship('ClassInfo', backref='teachingAssignment', lazy=False)

	semester_id = db.Column(db.Integer(), db.ForeignKey('semester.id'), nullable=False)
	semester = db.relationship('Semester', backref='teachingAssignment', lazy=False)

	school_year_id = db.Column(db.Integer(), db.ForeignKey('schoolyear.id'), nullable=False)
	school_year = db.relationship('SchoolYear', backref='schoolYear', lazy=False)

	transcript_info = db.relationship('SubjectTranscript', backref='teachingAssignment', lazy=False)
	created_at = db.Column(db.DateTime, nullable=False,
        default=datetime.now())

class ScoreType(db.Model):
	__tablename__ = 'scoretype'
	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	score_name = db.Column(db.String(length=100), nullable=False, unique=True)
	multiplier = db.Column(db.Integer(), nullable=False, default=1)
	active = db.Column(db.Boolean(), nullable=False, default=True)

class SubjectTranscript(db.Model):
	__tablename__ = 'subjecttranscript'
	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

	student_id = db.Column(db.Integer(),  db.ForeignKey('student.id'), primary_key=True)
	student = db.relationship('Student', backref='subjectTranscript', lazy=False)

	transcript_info_id = db.Column(db.Integer(), db.ForeignKey('teachingassignment.id'), nullable=False)
	transcrip_details = db.relationship('DetailsTranscript', backref='subjectTranscript', lazy=False)

	score_average = db.Column(db.Float(), nullable=True)
	created_at = db.Column(db.DateTime, nullable=False,
        default=datetime.now())

class DetailsTranscript(db.Model):
	__tablename__ = 'detailstranscript'
	transcript_id = db.Column(db.Integer(), db.ForeignKey('subjecttranscript.id'), primary_key=True)

	score_type_id = db.Column(db.Integer(), db.ForeignKey('scoretype.id'), primary_key=True)
	score_type = db.relationship('ScoreType', backref='detailsTranscript', lazy=False)

	score = db.Column(db.Float(), nullable=True)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
	modified_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
class Administrator(db.Model):
	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
	user = db.relationship('User', backref='administrator', lazy=False)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

class EducationalOffice(db.Model):
	__tablename__ = 'educationaloffice'
	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
	user = db.relationship('User', backref='educationalOffice', lazy=False)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

class InputScoreTime(db.Model):
	__tablename__ = 'inputscoretime'
	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	start_date = db.Column(db.DateTime(), nullable=False,unique=True)
	end_date = db.Column(db.DateTime(), nullable=False, unique=True)
	status = db.Column(db.Boolean(), nullable=False, default=False)

# --------------------------------------------------------------------------
# ------------------------FOR CONFIRM AND SUBMIT RESUME-----------------------

class ResumeImageFields(db.Model):
	__tablename__ = 'resumeimagefields'
	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	field_name = db.Column(db.String(length=100), nullable=False, unique=True)
	role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='SET NULL'), nullable=True)
	role = db.relationship('Role', backref='resumeImageFields', lazy=False)

class Resume(db.Model):
	__tablename__ = 'resume'
	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True)
	user = db.relationship('User', backref='resume', lazy=False)
	uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
	modified_at = db.Column(db.DateTime, nullable=True, default=datetime.now())
	confirmed_at = db.Column(db.DateTime, nullable=True)
	status = db.Column(db.Integer, nullable=False, default=0)

class ResumeImageStorage(db.Model):
	__tablename__ = 'resumeimagestorage'
	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	resume_id = db.Column(db.Integer(), db.ForeignKey('resume.id', ondelete='SET NULL'), nullable=True)
	resume = db.relationship('Resume', backref='resumeImageStorage', lazy=False)
	field_id = db.Column(db.Integer(), db.ForeignKey('resumeimagefields.id', ondelete='SET NULL'), nullable=True)
	field = db.relationship('ResumeImageFields', backref='resumeImageStorage', lazy=False)
	image_path = db.Column(db.String(length=200), nullable=True)
	image_public_id = db.Column(db.String(length=100), nullable=True)


