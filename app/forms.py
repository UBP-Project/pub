from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import Required
from wtforms.fields.html5 import EmailField, DateField
from wtforms.widgets import TextArea
from flask_wtf.file import FileField, FileRequired
from .models import Interest_Group, Role


class LoginForm(FlaskForm):
    email = StringField("Email or Username", validators=[Required()])
    password = PasswordField("Password", validators=[Required()])
    submit = SubmitField("SUBMIT")

class UserFormMixin():
    firstname  = StringField("First name", validators=[Required()])
    middlename = StringField("Middle name", validators=[Required()])
    lastname   = StringField("Last name", validators=[Required()])
    email      = EmailField("Email", validators=[Required()])
    department = StringField("Department", validators=[Required()])
    position   = StringField("Position", validators=[Required()])
    birthday   = DateField("Birthday", validators=[Required()])

class CreateUserForm(FlaskForm, UserFormMixin):
    role       = SelectField('Role', choices=[], coerce=int)
    password   = PasswordField("Password", validators=[Required()])
    submit     = SubmitField("Create User")

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.all() if role.name != 'Administrator']

class UpdateUserForm(FlaskForm, UserFormMixin):
    role       = SelectField('Role', choices=[], coerce=int)
    submit     = SubmitField("Update Information")

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.all() if role.name != 'Administrator']

class UpdateUserFormClient(FlaskForm, UserFormMixin):
    submit     = SubmitField("Update Information")

class PasswordForm(FlaskForm):
    password = PasswordField("Password")
    submit   = SubmitField("Change Password")

class PasswordFormClient(FlaskForm):
    old_password = PasswordField("Old Password")
    new_password = PasswordField("New Password")
    submit = SubmitField("Change Password")

class InterestGroupMixin():
    name        = StringField("Group Name", validators=[Required()])
    about       = StringField("About Group", widget=TextArea(), validators=[Required()])

class CreateInterestGroupForm(FlaskForm, InterestGroupMixin):
    cover_photo = FileField("Cover Photo", validators=[FileRequired()])
    group_icon  = FileField("Group Icon", validators=[FileRequired()])
    submit      = SubmitField("Create Interest Group")

class UpdateInterestGroupForm(FlaskForm, InterestGroupMixin):
    cover_photo = FileField("Cover Photo")
    group_icon  = FileField("Group Icon")
    submit = SubmitField("Save Changes")

class ActivityMixin():
    title       = StringField("Activity Title", validators=[Required()])
    description = StringField("Activity Description", widget=TextArea(), validators=[Required()])
    start_date  = DateField("Start Date", validators=[Required()])
    end_date    = DateField("End Date", validators=[Required()])
    address     = StringField("Address", validators=[Required()])
    group       = SelectField('Group', choices=[], coerce=int)

class CreateActivityForm(FlaskForm, ActivityMixin):
    image = FileField("Activity Image", validators=[FileRequired()])
    submit      = SubmitField("Create Activity")

    def __init__(self, *args, **kwargs):
        super(CreateActivityForm, self).__init__(*args, **kwargs)
        self.group.choices = [(0, "None")] + [(group.id, group.name) for group in Interest_Group.query.all()]

class UpdateActivityForm(FlaskForm, ActivityMixin):
    image       = FileField("Activity Image")
    submit      = SubmitField("Save Changes")

    def __init__(self, *args, **kwargs):
        super(UpdateActivityForm, self).__init__(*args, **kwargs)
        self.group.choices = [(0, "None")] + [(group.id, group.name) for group in Interest_Group.query.all()]

class GroupMembershipForm(FlaskForm):
    join_group = SubmitField("Join Group")
    leave_group = SubmitField("Leave Group")



