from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from form import FromBooking, RadioRequest


app = Flask(__name__)
app.secret_key = "random-string"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# models
class Booking(db.Model):
    __tablename__ = "booking"

    id = db.Column(db.Integer, primary_key=True)

    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    teacher = db.relationship("Teacher")

    day_id = db.Column(db.Integer, db.ForeignKey("day.id"))
    day = db.relationship("Day")

    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))
    student = db.relationship("Student")

    time_id = db.Column(db.Integer, db.ForeignKey("time.id"))
    time = db.relationship("Time")


class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.String)
    rating = db.Column(db.Float, nullable=False)
    picture = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.Boolean, nullable=False)

    book = db.relationship("Booking")


class GoalTeacher(db.Model):
    __tablename__ = "goalsteachers"

    id = db.Column(db.Integer, primary_key=True)

    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    teacher = db.relationship("Teacher")

    goal_id = db.Column(db.Integer, db.ForeignKey("goals.id"))
    goal = db.relationship("Goal")


class Goal(db.Model):
    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


class Day(db.Model):
    __tablename__ = "day"

    id = db.Column(db.Integer, primary_key=True)
    week_day = db.Column(db.String, nullable=False)
    book = db.relationship("Booking")


class Time(db.Model):
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


@app.route('/')
def render_main():

    teacher = db.session.query(Teacher).limit(6)
    get_goals = db.session.query(Goal.name).all()

    clear_goals = []
    for goal in get_goals:
        clear_goals.append(goal[0])

    return render_template('index.html', four_teach=teacher, goals=clear_goals)


@app.route('/goals/<goal>/')
def render_goals_page(goal):

    get_goals = db.session.query(Goal.name).all()

    clear_goals = []
    for now_goal in get_goals:
        clear_goals.append(now_goal[0])

    get_goal_id = db.session.query(Goal.id).filter(Goal.name == goal).first()[0]

    teacher_for_goals = db.session.query(Teacher).join(GoalTeacher).join(Goal).filter(GoalTeacher.goal_id == get_goal_id).all()

    return render_template('goal.html', teachers=teacher_for_goals, goals=clear_goals)


@app.route('/profiles/<int:id_teacher>/')
def render_profiles_page(id_teacher):

    teacher = db.session.query(Teacher).get(id_teacher)
    days = db.session.query(Day.week_day).all()
    times = db.session.query(Time.time).all()

    booking = db.session.query(Booking.teacher_id, Day.week_day, Time.time).join(Teacher).join(Time).join(Day).filter(Teacher.id == id_teacher).all()
    allready = []
    for booking in booking:
        allready.append((booking[1], booking[2]))

    time = []
    for now_time in times:
        time.append(now_time[0])
    day = []
    for now_day in days:
        day.append(now_day[0])

    return render_template('profile.html', allready=allready, name=teacher.name, about=teacher.about, rating=teacher.rating, price=teacher.price, picture=teacher.picture, day=day, id_teacher=id_teacher, time=time)


@app.route('/booking/<int:id_teacher>/<w_day>/<time>/', methods=['GET', 'POST'])
def render_booking_page(id_teacher, w_day, time):

    teacher = db.session.query(Teacher).get(id_teacher)

    form = FromBooking()
    name = form.name.data
    phone = form.phone.data

    if form.validate_on_submit():
        if db.session.query(Student).filter(Student.phone == phone).first():

            nik = db.session.query(Student.id).filter(Student.phone == phone).first()[0]
            now_day = db.session.query(Day.id).filter(Day.week_day == w_day).first()[0]
            now_time = db.session.query(Time.id).filter(Time.time == time).first()[0]

            booking = Booking(teacher_id=id_teacher, student_id=nik, day_id=now_day, time_id=now_time)
            db.session.add(booking)
            db.session.commit()
        else:
            student = Student(name=name, phone=phone)
            db.session.add(student)
            db.session.commit()

            nik = db.session.query(Student.id).filter(Student.phone == phone).first()[0]
            now_day = db.session.query(Day.id).filter(Day.week_day == w_day).first()[0]
            now_time = db.session.query(Time.id).filter(Time.time == time).first()[0]

            booking = Booking(teacher_id=id_teacher, student_id=nik, day_id=now_day, time_id=now_time)
            db.session.add(booking)
            db.session.commit()

        return render_template('booking_done.html', name=name, time=time, day=w_day, phone=phone)
    return render_template('booking.html', id_teacher=id_teacher, w_day=w_day, time=time, name=teacher.name, id=teacher.id, form=form)


@app.route('/request/', methods=['GET', 'POST'])
def render_request_page():
    radio = RadioRequest()
    for_what = int(radio.for_what.data)
    gender = radio.gender.data
    teacher_gender = gender == 'True'
    teacher_for_filter = db.session.query(Teacher).join(GoalTeacher).join(Goal).filter(db.and_(GoalTeacher.goal_id == for_what, Teacher.gender == teacher_gender)).all()
    if radio.validate_on_submit():
        if len(teacher_for_filter) == 0:
            text = 'Мы не нашли преподавателя по вашему запросу. Попробуйте позже.'
            return render_template('request_done.html', text=text)
        return render_template('request_done.html', teachers=teacher_for_filter)
    else:
        return render_template('request.html', form=radio)


if __name__ == '__main__':
    app.run('0.0.0.0', 8000)

