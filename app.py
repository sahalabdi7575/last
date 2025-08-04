from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# Student Table
class studentstbl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    faculty = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.String(100), nullable=False)
#teachers table
class teacherstbl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    
#other staff table
class stafftbl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(100), nullable=False)
    
# read data
@app.route('/')
def index():
    students = studentstbl.query.all()
    return render_template("students.html", students=students)

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    faculty = request.form['faculty']
    semester = request.form['semester']
    student = studentstbl(name=name,faculty=faculty,semester=semester)
    db.session.add(student)
    db.session.commit()
    return redirect(url_for('index'))

# teacher's read data
@app.route('/teachers')
def show_teachers():
    teachers = teacherstbl.query.all()
    return render_template("teachers.html", teachers=teachers)

@app.route('/add_teacher', methods=['POST'])
def add_teacher():
    name = request.form['name']
    phone = request.form['phone']
    teacher = teacherstbl(name=name,phone=phone)
    db.session.add(teacher)
    db.session.commit()
    return redirect(url_for('show_teachers'))

# read data
@app.route('/staff')
def show_staff():
    staffs = stafftbl.query.all()
    return render_template("staff.html", staffs=staffs)

@app.route('/add_staff', methods=['POST'])
def add_staff():
    name = request.form['name']
    position = request.form['position']
    salary = request.form['salary']
    staff = stafftbl(name=name,position=position,salary=salary)
    db.session.add(staff)
    db.session.commit()
    return redirect(url_for('show_staff'))

#delete student
@app.route('/delete_student/<int:student_id>',methods=['POST'])
def delete_student(student_id):
    student=studentstbl.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

#update
@app.route('/edit_student/<int:student_id>',methods=['POST','GET'])
def edit_student(student_id):
    student=studentstbl.query.get_or_404(student_id)
    if request.method=='POST':
        student.name=request.form['name']
        student.faculty=request.form['faculty']
        student.semester=request.form['semester']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_student.html',student=student)
    




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
