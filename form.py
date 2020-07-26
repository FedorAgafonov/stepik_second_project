from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import InputRequired, Length


class FromBooking(FlaskForm):
    name = StringField('Вас зовут', [InputRequired(message="Введите что-нибудь")])
    phone = StringField('Ваш телефон', [Length(min=10, message="Некорректный номер")])
    submit = SubmitField('Записаться на пробный урок')


class RadioRequest(FlaskForm):
    for_what = RadioField('Какая цель занятий?', choices=[("1", "Для путешествий"), ("2", "Для школы"), ("3", "Для работы"), ("4", "Для переезда"), ("5", "Для программирования")], default='1')
    how_time = RadioField('Сколько времени есть?', choices=[("1-2", "1-2 часа в неделю"), ("3-5", "3-5 часов в неделю"), ("5-7", "5-7 часов в неделю"), ("7-10", "7-10 часов в неделю")], default='3-5')
    gender = RadioField('Пол преподавателя?', choices=[("True", "Мужчина"), ("False", "Женщина")], default='True')
    submit = SubmitField('Найдите мне преподавателя')
