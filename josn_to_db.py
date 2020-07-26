import json
from app import Teacher, Day, Time, db, Goal, GoalTeacher


def json_to_db():

    with open('data/teachers.json', 'r') as teach:
        get_data = json.load(teach)

    for item in get_data:
        gender = item['gender']

        teacher = Teacher(name=item['name'], about=item['about'], rating=item['rating'], picture=item['picture'], price=item['price'], gender=gender)
        db.session.add(teacher)

    for days in get_data[0]['free']:
        day = Day(week_day=days)
        db.session.add(day)

    for time in get_data[0]['free']['mon']:
        times = Time(time=time)
        db.session.add(times)

    for goal in goals:
        goals = Goal(name=goal)
        db.session.add(goals)

    for teacher in get_data:
        teacher_goals = teacher['goals']
        for goal in teacher_goals:
            get_goal_id = db.session.query(Goal.id).filter(Goal.name == goal).first()[0]
            teacher_id = int(teacher['id']) + 1
            goal_teacher = GoalTeacher(teacher_id=teacher_id, goal_id=get_goal_id)
            db.session.add(goal_teacher)

    db.session.commit()


if __name__ == '__main__':
    json_to_db()
