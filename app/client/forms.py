from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField("Email or Username", validators=[Required()])
    password = PasswordField("Password")
    submit = SubmitField("SUBMIT")
