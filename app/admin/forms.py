from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import Required
from ..models import Interest_Group


class CreateInterestGroupForm(Form):
    name = StringField('Group name', validators=[Required()])
    submit = SubmitField('Submit')

class CreateUserForm(Form):
    firstname  = StringField("First name", validators=[Required()])
    middlename = StringField("Middle name")
    lastname   = StringField("Last name")
    email      = StringField("Email")
    password   = PasswordField("Password")
    department = StringField("Department")
    position   = StringField("Position")
    birthday   = DateField("Birthday")
    submit     = SubmitField("Submit")

class CreateInterestGroupForm(Form):
    name        = StringField("Group Name", validators=[Required()])
    about       = StringField("About Group")
    cover_photo = StringField("Cover Photo")
    group_icon  = StringField("Group Icon")
    submit      = SubmitField("Submit")

class CreateActivityForm(Form):
    title       = StringField("Activity Title", validators=[Required()])
    description = StringField("Activity Description")
    start_date  = DateField("Start Date")
    end_date    = DateField("End Date")
    address     = StringField("Address")
    group_id    = SelectField("Group ID", choices=[(None, "No Group")])
    submit      = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super(CreateActivityForm, self).__init__(*args, **kwargs)
        self.group_id.choices = [(None, "No Group")] + [(str(group.id), group.name) for group in Interest_Group.query.all()]



