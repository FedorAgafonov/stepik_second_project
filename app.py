import json
from flask import Flask, render_template
from form import FromBooking, RadioRequest

app = Flask(__name__)
app.secret_key = "random-string"

week_days = {
    'mon': 'Monday',
    'tue': 'Tuesday',
    'wed': 'Wednesday',
    'thu': 'Thursday',
    'fri': 'Friday',
    'sat': 'Saturday',
    'sun': 'Sunday'
}


def read_json(url):
    with open('data/' + url + '.json', 'r') as teach:
        data = json.load(teach)
    return data


def write_json(url, some):
    with open('data/' + url + '.json', 'w') as write_f:
        write_f.write(some)


@app.route('/')
def render_main():

    teachers = read_json('teachers')
    goals = read_json('goals')

    return render_template('index.html', four_teach=teachers[:6], goal=goals)


@app.route('/goals/<goal>/')
def render_goals_page(goal):

    teachers = read_json('teachers')

    goals = read_json('goals')
    necessary_teacher = []
    for item in teachers:
        if goal in item['goals']:
            necessary_teacher.append(item)
    goal = goals[goal]
    return render_template('goal.html', teachers=necessary_teacher, goal=goal.lower())


@app.route('/profiles/<int:id_teacher>/')
def render_profiles_page(id_teacher):

    data = read_json('teachers')

    for item in data:
        if item['id'] == id_teacher:
            data = item
            break
    free_days = {}
    for key, item in data['free'].items():
        free_days[key] = item
    return render_template('profile.html', id_teacher=id_teacher, data_of_teacher=data, free_days=free_days, week=week_days)


@app.route('/request/', methods=['GET', 'POST'])
def render_request_page():
    radio = RadioRequest()
    name = radio.name.data
    phone = radio.phone.data
    for_what = radio.for_what.data
    how_time = radio.how_time.data
    if radio.validate_on_submit():

        data_request = read_json('request')
        data_request.append({'name': name, 'phone': phone, 'for_what': for_what, 'how_time': how_time})
        contents = json.dumps(data_request, indent=4, ensure_ascii=False)
        write_json('request', contents)

        return render_template('request_done.html', name=name, phone=phone, for_what=for_what, how_time=how_time)
    else:
        return render_template('request.html', form=radio)


@app.route('/booking/<int:id_teacher>/<w_day>/<time>/', methods=['GET', 'POST'])
def render_booking_page(id_teacher, w_day, time):

    data = read_json('teachers')
    for item in data:
        if item['id'] == id_teacher:
            data = item
            break

    form = FromBooking()
    name = form.name.data
    phone = form.phone.data

    if form.validate_on_submit():
        data_phone = read_json('booking')
        data_phone.append({'name': name, 'phone': phone})
        contents = json.dumps(data_phone, indent=4, ensure_ascii=False)
        write_json('booking', contents)
        return render_template('booking_done.html', name=name, time=time, day=w_day, phone=phone, week=week_days)
    return render_template('booking.html', id_teacher=id_teacher, w_day=w_day, time=time, data_of_teacher=data, week=week_days, form=form)


if __name__ == '__main__':
    app.run()
