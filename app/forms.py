from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import Required
from wtforms.fields.html5 import EmailField, DateField
from wtforms.widgets import TextArea
from flask_wtf.file import FileField
from .models import Interest_Group


class LoginForm(FlaskForm):
    email = StringField("Email or Username", validators=[Required()])
    password = PasswordField("Password")
    submit = SubmitField("SUBMIT")

class UserFormMixin():
    firstname  = StringField("First name", validators=[Required()])
    middlename = StringField("Middle name")
    lastname   = StringField("Last name")
    email      = EmailField("Email")
    password   = PasswordField("Password")
    department = StringField("Department")
    position   = StringField("Position")
    birthday   = DateField("Birthday")
    role       = SelectField('Role', choices=[('1', 'Default'), ('2', 'Manager')])

class CreateUserForm(FlaskForm, UserFormMixin):
    submit     = SubmitField("Create User")

class UpdateUserForm(FlaskForm, UserFormMixin):
    submit     = SubmitField("Update User")

class InterestGroupMixin():
    name        = StringField("Group Name")
    about       = StringField("About Group")
    cover_photo = FileField("Cover Photo")
    group_icon  = FileField("Group Icon")

class CreateInterestGroupForm(FlaskForm, InterestGroupMixin):
    submit      = SubmitField("Create Interest Group")

class UpdateInterestGroupForm(FlaskForm, InterestGroupMixin):
    submit = SubmitField("Save Changes")

class ActivityMixin():
    title       = StringField("Activity Title")
    description = StringField("Activity Description", widget=TextArea())
    start_date  = DateField("Start Date")
    end_date    = DateField("End Date")
    address     = StringField("Address")
    group       = SelectField('Group', choices=[], coerce=int)

class CreateActivityForm(FlaskForm, ActivityMixin):
    submit      = SubmitField("Create Activity")

    def __init__(self, *args, **kwargs):
        super(CreateActivityForm, self).__init__(*args, **kwargs)
        self.group.choices = [(0, "None")] + [(group.id, group.name) for group in Interest_Group.query.all()]

class UpdateActivityForm(FlaskForm, ActivityMixin):
    submit      = SubmitField("Save Changes")

    def __init__(self, *args, **kwargs):
        super(UpdateActivityForm, self).__init__(*args, **kwargs)
        self.group.choices = [(None, "None")] + [(group.id, group.name) for group in Interest_Group.query.all()]

class GroupMembershipForm(FlaskForm):
    join_group = SubmitField("Join Group")
    leave_group = SubmitField("Leave Group")



