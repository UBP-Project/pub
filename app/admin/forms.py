from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required


class CreateInterestGroupForm(FlaskForm):
    name = StringField('Group name', validators=[Required()])
    submit = SubmitField('Submit')

class CreateUserForm(FlaskForm):
    firstname  = StringField("First name", validators=[Required()])
    middlename = StringField("Middle name")
    lastname   = StringField("Last name")
    email      = StringField("Email")
    password   = PasswordField("Password")
    department = StringField("Department")
    position   = StringField("Position")
    birthday   = StringField("Birthday")
    submit     = SubmitField("Submit")

class CreateInterestGroupForm(FlaskForm):
    name        = StringField("Group Name")
    about       = StringField("About Group")
    cover_photo = StringField("Cover Photo")
    group_icon  = StringField("Group Icon")
    submit      = SubmitField("Submit")

