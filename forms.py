from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('email', validators=[Email()])
    password = StringField('password', validators=[DataRequired(), Length(min=4, max=30)])


class SingUpForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[Email()])
    password = StringField('password', validators=[DataRequired(), Length(min=4, max=30)])