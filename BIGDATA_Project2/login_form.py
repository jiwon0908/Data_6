from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('아이디', validators=[DataRequired()])
    password = StringField('비밀번호', validators=[DataRequired()])
    remember_me = BooleanField('로그인 유지')
    submit = SubmitField('로그인')