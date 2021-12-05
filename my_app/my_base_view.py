from my_app.admin import *

class MyBaseView(ModelView):

	def is_accessible(self):
		return current_user.is_authenticated and current_user.is_admin()
	
	def inaccessible_callback(self, name, **kwargs):
		flash('Yêu cầu truy cập không khả dụng!! Hãy đăng nhập', category='danger')
		return redirect(url_for('login_page'))

	form_excluded_columns = ('created_at','modified_at', 'teachingAssignment', 'schoolYear', 'detailsTranscript', 'class')

	list_template = 'admin/list.html'
	column_labels = {
		'id': 'ID',
		'user.image': 'Hình ảnh',
		'teacher_code': 'Mã GV',
		'student_code': 'Mã HS',
		'subject': 'Môn  phụ trách',
		'classInfo': 'Lớp',
		'semester': 'Học kỳ',
		'user.full_name': 'Họ và tên',
		'full_name': 'Họ và tên',
		'user.gender': 'Giới tính',
		'gender': 'Giới tính',
		'user.role': 'Role',
		'role': 'Role',
		'user.birthdate': 'Ngày sinh',
		'birthdate': 'Ngày sinh',
		'user.ethnic': 'Dân tộc',
		'ethnic': 'Dân tộc',
		'user.nationality': 'Quốc tịch',
		'nationality': 'Quốc tịch',
		'user.permanent_address': 'Địa chỉ thường trú',
		'permanent_address': 'Địa chỉ thường trú',
		'user.home_town': 'Quê quán',
		'home_town': 'Quê quán',
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
		'student' : 'Mã HS',
		'class_info': 'Lớp',
		'start_date': 'Ngày bắt đầu',
		'end_date': 'Ngày kết thúc',
		'status': 'Tình trạng'

	}
	form_widget_args = {
        'student_code': {
            'readonly': True
        },
        'teacher_code': {
            'readonly': True
        },
    }
