# app.py (Updated)
import sys
from datetime import datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
with app.app_context():
    db = SQLAlchemy(app)

    class Student(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        first_name = db.Column(db.String(50), nullable=False)
        last_name = db.Column(db.String(50), nullable=False)
        dob = db.Column(db.Date, nullable=False)
        amount_due = db.Column(db.Float, default=0.0)

        def __repr__(self):
            return f"<Student {self.id}: {self.first_name} {self.last_name}>"

    # Create the database tables
    db.create_all()

    # Routes for rendering HTML pages

    @app.route('/')
    def index():
        students = Student.query.all()
        return render_template('index.html', students=students)

    @app.route('/add', methods=['GET', 'POST'])
    def add_student():
        if request.method == 'POST':
            data = request.form
            # print(data['dob'])
            # sys.exit()
            student = Student(
                first_name=data['first_name'],
                last_name=data['last_name'],
                dob=datetime.strptime(data['dob'], "%Y-%m-%d").date(),
                amount_due=data['amount_due']
            )
            db.session.add(student)
            db.session.commit()
            return redirect(url_for('index'))

        return render_template('add_student.html')

    @app.route('/view/<int:student_id>')
    def view_student(student_id):
        student = Student.query.get(student_id)
        if not student:
            return jsonify({"message": "Student not found"}), 404

        return render_template('view_student.html', student=student)

    @app.route('/edit/<int:student_id>', methods=['GET', 'POST'])
    def edit_student(student_id):
        student = Student.query.get(student_id)
        if not student:
            return jsonify({"message": "Student not found"}), 404

        if request.method == 'POST':
            data = request.form
            student.first_name = data['first_name']
            student.last_name = data['last_name']
            student.dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
            student.amount_due = data['amount_due']
            db.session.commit()
            return redirect(url_for('view_student', student_id=student.id))

        return render_template('edit_student.html', student=student)

    @app.route('/delete/<int:student_id>', methods=['GET', 'POST'])
    def delete_student(student_id):
        student = Student.query.get(student_id)
        if not student:
            return jsonify({"message": "Student not found"}), 404

        if request.method == 'POST':
            db.session.delete(student)
            db.session.commit()
            return redirect(url_for('index'))

        return render_template('delete_student.html', student=student)


if __name__ == '__main__':
    app.run(debug=True)
