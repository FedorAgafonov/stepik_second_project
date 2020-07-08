import json
from flask import Flask, render_template
from form import FromBooking, RadioRequest

app = Flask(__name__)
app.secret_key = "randomstring"

week_days = {
    'mon': 'Monday',
    'tue': 'Tuesday',
    'wed': 'Wednesday',
    'thu': 'Thursday',
    'fri': 'Friday',
    'sat': 'Saturday',
    'sun': 'Sunday'
}


@app.route('/')
def render_main():
    return render_template('index.html')


@app.route('/goals/<goal>/')
def render_goals_page(goal):
    return render_template('goal.html')


@app.route('/profiles/<int:id_teacher>/')
def render_profiles_page(id_teacher):
    with open('data/teachers.json', 'r') as teach:
        data = json.load(teach)
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
    phone = phone.replace('-', "")
    for_what = radio.for_what.data
    how_time = radio.how_time.data
    if radio.validate_on_submit():

        with open('data/request.json', 'r') as read_f:
            data_request = json.load(read_f)
        data_request.append({'name': name, 'phone': phone, 'for_what': for_what, 'how_time': how_time})
        with open('data/request.json', 'w') as write_f:
            contents = json.dumps(data_request, indent=4, ensure_ascii=False)
            write_f.write(contents)

        return render_template('request_done.html', name=name, phone=phone, for_what=for_what, how_time=how_time)
    else:
        print(radio.errors)
        return render_template('request.html', form=radio)


@app.route('/booking/<int:id_teacher>/<w_day>/<time>/')
def render_booking_page(id_teacher, w_day, time):
    with open('data/teachers.json', 'r') as teach:
        data = json.load(teach)
        for item in data:
            if item['id'] == id_teacher:
                data = item
                break
    form = FromBooking()
    return render_template('booking.html', id_teacher=id_teacher, w_day=w_day, time=time, data_of_teacher=data, week=week_days, form=form)


@app.route('/booking_done/<day>/<int:time>/', methods=['POST'])
def render_booking_done(day, time):
    form = FromBooking()
    name = form.name.data
    phone = form.phone.data
    with open('data/booking.json', 'r') as read_f:
        data_phone = json.load(read_f)
    data_phone.append({'name': name, 'phone': phone})
    with open('data/booking.json', 'w') as write_f:
        contents = json.dumps(data_phone, indent=4, ensure_ascii=False)
        write_f.write(contents)
    return render_template('booking_done.html', name=name, time=time, day=day, phone=phone, week=week_days)


app.run()
