import json
import os
from flask import Flask, render_template
from form import FromBooking, RadioRequest
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "random-string"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# models
class Booking(db.Model):
    __tablename__ = "booking"

    id = db.Column(db.Integer, primary_key=True)

    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    teacher = db.relationship("Teachers")

    day_id = db.Column(db.Integer, db.ForeignKey("day.id"))
    day = db.relationship("Day")

    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))
    day = db.relationship("Student")

    time_id = db.Column(db.Integer, db.ForeignKey("time.id"))
    time = db.relationship("Times")


class Teachers(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.String)
    rating = db.Column(db.Float, nullable=False)
    picture = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Boolean, nullable=False)

    travel = db.Column(db.Boolean, nullable=False)
    study = db.Column(db.Boolean, nullable=False)
    work = db.Column(db.Boolean, nullable=False)
    program = db.Column(db.Boolean, nullable=False)
    relocate = db.Column(db.Boolean, nullable=False)

    book = db.relationship("Booking")


class Day(db.Model):
    __tablename__ = "day"

    id = db.Column(db.Integer, primary_key=True)
    week_day = db.Column(db.String, nullable=False)
    book = db.relationship("Booking")


class Times(db.Model):
    __tablename__ = "time"

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String)

    book = db.relationship("Booking")


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False, unique=True)

    book = db.relationship("Booking")


# db.create_all()
#
# with open('data/teachers.json', 'r') as teach:
#     get_data = json.load(teach)
#
# for item in get_data:
#     travel = 'travel' in get_data[item['id']]['goals']
#     relocate = 'relocate' in get_data[item['id']]['goals']
#     study = 'study' in get_data[item['id']]['goals']
#     program = 'program' in get_data[item['id']]['goals']
#     work = 'work' in get_data[item['id']]['goals']
#     gender = item['gender']
#     teacher = Teachers(name=item['name'], about=item['about'], rating=item['rating'], picture=item['picture'], price=item['price'], gender=gender, travel=travel, relocate=relocate, study=study, program=program, work=work)
#     db.session.add(teacher)
#
# for days in get_data[0]['free']:
#     print(days)
#     day = Day(week_day=days)
#     db.session.add(day)
#
# for time in get_data[0]['free']['mon']:
#     print(time)
#     times = Times(time=time)
#     db.session.add(times)
#
# db.session.commit()

# get end

# models end

goals = {
    "travel": "Для путешествий",
    "study": "Для учебы",
    "work": "Для работы",
    "relocate": "Для переезда",
    "program": "Для программирования"
}


@app.route('/')
def render_main():

    teachers = db.session.query(Teachers).all()

    return render_template('index.html', four_teach=teachers, goal=goals)


@app.route('/goals/<goal>/')
def render_goals_page(goal):

    teacher = db.session.query(Teachers).all()
    if goal == 'travel':
        teacher = db.session.query(Teachers).filter(Teachers.travel == True).all()
    elif goal == 'study':
        teacher = db.session.query(Teachers).filter(Teachers.study == True).all()
    elif goal == 'work':
        teacher = db.session.query(Teachers).filter(Teachers.work == True).all()
    elif goal == 'program':
        teacher = db.session.query(Teachers).filter(Teachers.program == True).all()
    return render_template('goal.html', teachers=teacher, goal=goal.lower(), goals=goals)


@app.route('/profiles/<int:id_teacher>/')
def render_profiles_page(id_teacher):

    teacher = db.session.query(Teachers).get(id_teacher)
    days = db.session.query(Day.week_day).all()
    times = db.session.query(Times.time).all()

    booking = db.session.query(Booking.teacher_id, Day.week_day, Times.time).join(Teachers).join(Times).join(Day).filter(Teachers.id == id_teacher).all()
    allready = []
    for booking in booking:
        allready.append((booking[1], booking[2]))

    time = []
    for s in times:
        time.append(s[0])
    day = []
    for s in days:
        day.append(s[0])

    return render_template('profile.html', allready=allready, name=teacher.name, about=teacher.about, rating=teacher.rating, price=teacher.price, picture=teacher.picture, day=day, id_teacher=id_teacher, time=time)


@app.route('/booking/<int:id_teacher>/<w_day>/<time>/', methods=['GET', 'POST'])
def render_booking_page(id_teacher, w_day, time):

    teacher = db.session.query(Teachers).get(id_teacher)

    form = FromBooking()
    name = form.name.data
    phone = form.phone.data

    if form.validate_on_submit():
        name.replace(' ', '')
        phone.replace(' ', '')
        if db.session.query(Student).filter(Student.name == name).all() or db.session.query(Student).filter(Student.phone == phone).all():
            nik = db.session.query(Student.id).filter(Student.name == name).all()
            now_day = db.session.query(Day.id).filter(Day.week_day == w_day).all()
            now_time = db.session.query(Times.id).filter(Times.time == time).all()
            booking = Booking(teacher_id=id_teacher, student_id=nik[0][0], day_id=now_day[0][0], time_id=now_time[0][0])
            db.session.add(booking)
            db.session.commit()
        else:
            student = Student(name=name, phone=phone)
            db.session.add(student)
            db.session.commit()
            nik = db.session.query(Student.id).filter(Student.name == name).all()
            now_day = db.session.query(Day.id).filter(Day.week_day == w_day).all()
            now_time = db.session.query(Times.id).filter(Times.time == time).all()
            booking = Booking(teacher_id=id_teacher, student_id=nik[0][0], day_id=now_day[0][0], time_id=now_time[0][0])
            db.session.add(booking)
            db.session.commit()

        return render_template('booking_done.html', name=name, time=time, day=w_day, phone=phone)
    return render_template('booking.html', id_teacher=id_teacher, w_day=w_day, time=time, name=teacher.name, id=teacher.id, form=form)


@app.route('/request/', methods=['GET', 'POST'])
def render_request_page():
    radio = RadioRequest()
    for_what = radio.for_what.data
    gender = radio.gender.data
    if gender == 'True':
        gender = True
    else:
        gender = False
    if radio.validate_on_submit():
        if for_what == 'travel':
            teacher = db.session.query(Teachers).filter(db.and_(Teachers.travel == True, Teachers.gender == gender)).all()
        elif for_what == 'study':
            teacher = db.session.query(Teachers).filter(db.and_(Teachers.study == True, Teachers.gender == gender)).all()
        elif for_what == 'work':
            teacher = db.session.query(Teachers).filter(db.and_(Teachers.work == True, Teachers.gender == gender)).all()
        elif for_what == 'program':
            teacher = db.session.query(Teachers).filter(db.and_(Teachers.program == True, Teachers.gender == gender)).all()
        if len(teacher) == 0:
            text = 'Мы не нашли преподавателя по вашему запросу. Попробуйте позже.'
            return render_template('request_done.html', text=text)
        return render_template('request_done.html', teachers=teacher)
    else:
        print(1)
        return render_template('request.html', form=radio)


if __name__ == '__main__':
    app.run()
