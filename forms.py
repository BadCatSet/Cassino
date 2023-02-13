from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, EqualTo, NumberRange


class SignupForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired('Пустая почта')])
    username = StringField('Имя пользователя', validators=[DataRequired('Пустое имя пользователя')])
    password1 = PasswordField('Пароль', validators=[DataRequired('Пустой пароль')])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired('Пустой пароль'),
                                                              EqualTo('password1', 'Пароли разные')])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = StringField('Логин', validators=[DataRequired('Пустой логин')])
    password = PasswordField('Пароль', validators=[DataRequired('Пустой пароль')])
    submit = SubmitField('Войти')


class FreeForm(FlaskForm):
    money = IntegerField('Сколько', validators=[DataRequired('Не стесняйся, говори'),
                                                NumberRange(-1e8, 1e8,
                                                            'Не жирно тебе? У меня бд взорвется от таких чисел')])

    submit = SubmitField('Получить халяву')
