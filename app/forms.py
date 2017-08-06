from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import Required
from wtforms.fields.html5 import EmailField, DateField
from wtforms.widgets import TextArea


class LoginForm(FlaskForm):
    email = StringField("Email or Username", validators=[Required()])
    password = PasswordField("Password")
    submit = SubmitField("SUBMIT")

class CreateUserForm(FlaskForm):
    firstname  = StringField("First name", validators=[Required()])
    middlename = StringField("Middle name")
    lastname   = StringField("Last name")
    email      = EmailField("Email")
    password   = PasswordField("Password")
    department = StringField("Department")
    position   = StringField("Position")
    birthday   = DateField("Birthday")
    role       = SelectField('Role', choices=[('1', 'Default'), ('2', 'Manager')])
    submit     = SubmitField("Create User")

class CreateInterestGroupForm(FlaskForm):
    name        = StringField("Group Name")
    about       = StringField("About Group")
    cover_photo = StringField("Cover Photo")
    group_icon  = StringField("Group Icon")
    submit      = SubmitField("Create Interest Group")

class CreateActivity(FlaskForm):
    title       = StringField("Activity Title")
    description = StringField("Activity Description", widget=TextArea())
    start_date  = DateField("Start Date")
    end_date    = DateField("End Date")
    address     = StringField("Address")
    submit      = SubmitField("Create Activity")

class GroupMembershipForm(FlaskForm):
    join_group = SubmitField("Join Group")
    leave_group = SubmitField("Leave Group")



