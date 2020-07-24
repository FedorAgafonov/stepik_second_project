import json
from app import Teachers, Day, Times, db

db.session.query(Teachers).filter_by().delete()
db.session.query(Times).filter_by().delete()
db.session.query(Day).filter_by().delete()
db.session.commit()

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
