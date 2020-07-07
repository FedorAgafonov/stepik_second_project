import json
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def render_main():
    return render_template('index.html')


@app.route('/goals/<goal>/')
def render_goals_page(goal):
    return render_template('goal.html')


@app.route('/profiles/<int:id_teacher>/')
def render_main_page(id_teacher):
    with open('data/teachers.json', 'r') as teach:
        data = json.load(teach)
        for item in data:
            if item['id'] == id_teacher:
                data = item
                break
    free_days = {}
    for key, item in data['free'].items():
        free_days[key] = item
    return render_template('profile.html', id_teacher=id_teacher, data_of_teacher=data, free_days=free_days)


@app.route('/request/')
def render_request_page():
    return render_template('request.html')


@app.route('/request_done/')
def render_request_done():
    return render_template('request_done.html')


@app.route('/booking/<int:id_teacher>/<w_day>/<time>/')
def render_booking_page(id_teacher, w_day, time):
    return render_template('booking.html')


@app.route('/booking_done/')
def render_booking_done():
    return render_template('booking_done.html')


app.run()
