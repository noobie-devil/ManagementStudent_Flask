> **_NOTE:_**  All information, software structure is for reference only and is used for the course, please consider carefully before using it in real projects..

# Building an educational management website application

This is the final project of the Software Technology class

## Collaborators

- [@truongnguyenvan8801](https://github.com/truongnguyenvan8801) - truongnguyenvan8801@gmail.com
- [@Vinh-san](https://github.com/Vinh-san) - ngvinh0109@gmail.com
- [@quangbdhz](https://github.com/quangbdhz) - tranquangbdhz@gmail.com
- [@vtv1234](https://github.com/vtv1234) - thanhvinh09032001@gmail.com

## Contents

- [Features](https://github.com/truongnguyenvan8801/ManagementStudent_Flask#Features)
- [Tech](https://github.com/truongnguyenvan8801/ManagementStudent_Flask#Tech)
- [Diagrams](https://github.com/truongnguyenvan8801/ManagementStudent_Flask#Diagrams)
- [Installations](https://github.com/truongnguyenvan8801/ManagementStudent_Flask#Installations)
  + [Database](https://github.com/truongnguyenvan8801/ManagementStudent_Flask#Installations#Database)
  + [Project](https://github.com/truongnguyenvan8801/ManagementStudent_Flask#Installations#Project)
- [Testing](https://github.com/truongnguyenvan8801/ManagementStudent_Flask#Testing)


## Functions

- Student Management: CRUD, search for students.
- Teacher Management: CRUD, search for teachers.
- Class Management: CRUD class information by grade, school year, semester. Implement the allocation of students in a class, allocating class responsibilities to         teachers according to the subject they are teaching.
- Subject Management: CRUD subjects currently being taught in the system.
- Score Management: CRUD types of score, allow teachers to input score for students with the classes they are currently teaching.


## Tech

**Database:** MySQL

**Frontend:** HTML, CSS3, Bootstrap. Customize the UI to meet project's requirements from [GURU Able - Free Lite Admin Template](https://github.com/technext/guruable2)

**Backend:** using Python as the primary programming language. With support from the [<ins>Flask</ins>](https://flask.palletsprojects.com/en/2.1.x/) framework for building web services.

Besides, the project uses a number of open source projects to work properly:
- [<ins>Flask</ins>](https://flask.palletsprojects.com/en/2.1.x/) -  A micro-framework, Flask lets us build web services with very little overhead
- [<ins>WTForms</ins>](https://wtforms.readthedocs.io/en/3.0.x/) - a flexible forms validation and rendering library for Python web development!
- [<ins>PyMySQL</ins>](https://pypi.org/project/PyMySQL/#documentation) - This package contains a pure-Python MySQL client library
- [<ins>Flask-Admin</ins>](https://flask-admin.readthedocs.io/en/latest/) - Solves the boring problem of building an admin interface on top of an existing data model. With little effort, it lets you manage your web service’s data through a user-friendly interface.
- ...



## Diagrams

### Class Diagram

![App Screenshot](https://imgur.com/Ww3cmyU.png)

### Database Diagram

![App Screenshot](https://imgur.com/2ok4EEs.png)



## Installations

### Database

Open MySQL Workbench and create a database named "studentmanagementdb"

```bash
  CREATE DATABASE studentmanagementdb
```
![ảnh](https://user-images.githubusercontent.com/73820820/176401876-237e1445-ab9a-44e2-af45-8b2b4742796e.png)

On the ***Toolbar***, click on ***Server*** and select ***Data Import***

![ảnh](https://user-images.githubusercontent.com/73820820/176403520-a6669288-3e28-4d86-962f-8134619538c0.png)

In the ***Data Import*** tab:
  + At ***Import from Self-Contained File***, select [<ins>**Nhom05_ManagementStudentDB.sql**</ins>](https://drive.google.com/file/d/16CtT6XBCuZ6M1v4BoP3JxwrY2JGtMZY3/view?usp=sharing) file
  + At ***Default Target Schema***, select the database **studentmanagementdb** created
  
![ảnh](https://user-images.githubusercontent.com/73820820/176404972-b64bab6c-e9f2-4f18-b606-a4f061a5454a.png)

Switch to the "Import Progress" tab and select "Start Import"

![ảnh](https://user-images.githubusercontent.com/73820820/176406184-2b1ea49a-ea04-425e-9c4f-272a536048a8.png)


### Project

Access the directory containing the project and create a virtual environment

```bash
  virtualenv venv
```

Enable virtual environment

```bash
  .\venv\Scripts\activate
```

Install all libraries in requirements.txt file.

```bash
  pip install -r requirements.txt
```

Setting environment variables

```bash
  $env:FLASK_APP='run'
```
```bash
  $env:FLASK_DEBUG=1
```

Run project

```bash
  flask run
```



## Testing

After importing the sample data we created from [<ins>**Nhom05_ManagementStudentDB.sql**</ins>](https://drive.google.com/file/d/16CtT6XBCuZ6M1v4BoP3JxwrY2JGtMZY3/view?usp=sharing), for testing you can log in to the following accounts:

Role as an administrator:
+ Username: ADMIN
+ Password: Group05_Admin

Role as an educational office:
+ Username: EDUCATION
+ Password: Group05_Education

Role as a teacher:
+ Username: TEACHER
+ Password: Group05_Teacher

Role as a student:
+ Username: STUDENT
+ Password: Group05_Student



