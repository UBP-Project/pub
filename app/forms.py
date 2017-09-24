from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import Required, UUID
from wtforms.fields.html5 import EmailField, DateField
from wtforms.widgets import TextArea
from flask_wtf.file import FileField, FileRequired
from .models import Interest_Group, Role, Membership
from flask_login import current_user


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
    image    = FileField("Image", validators=[FileRequired()])
    role     = SelectField('Role', choices=[], validators=[UUID()])
    password = PasswordField("Password", validators=[Required()])
    submit   = SubmitField("Create User")

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.role.choices = [(str(role.id), role.name) for role in Role.query.all() if role.name != 'Administrator']

class UpdateUserForm(FlaskForm, UserFormMixin):
    image  = FileField("Image")
    role   = SelectField('Role', choices=[])
    submit = SubmitField("Update Information")

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.role.choices = [(str(role.id), role.name) for role in Role.query.all() if role.name != 'Administrator']

class UpdateUserFormClient(FlaskForm, UserFormMixin):
    image  = FileField("Image")
    submit = SubmitField("Update Information")

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
    leader_ids  = StringField("Leader Ids")

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
    group       = SelectField('Group', choices=[])

class CreateActivityForm(FlaskForm, ActivityMixin):
    image = FileField("Activity Image", validators=[FileRequired()])
    submit = SubmitField("Create Activity")

    def __init__(self, *args, **kwargs):
        super(CreateActivityForm, self).__init__(*args, **kwargs)
        self.group.choices = [(None, None)] + [(str(group.id), group.name) for group in Interest_Group.query.all()]

class CreateActivityFormClient(FlaskForm, ActivityMixin):
    image = FileField("Activity Image", validators=[FileRequired()])
    submit = SubmitField("Create Activity")

    def __init__(self, *args, **kwargs):
        super(CreateActivityFormClient, self).__init__(*args, **kwargs)
        groups = Interest_Group.query.join(Membership, Membership.group_id == Interest_Group.id)\
            .filter(Membership.level == 1).all()
        self.group.choices = [(str(group.id), group.name) for group in groups]
        print("Choices", self.group.choices)

class UpdateActivityForm(FlaskForm, ActivityMixin):
    image       = FileField("Activity Image")
    submit      = SubmitField("Save Changes")

    def __init__(self, *args, **kwargs):
        super(UpdateActivityForm, self).__init__(*args, **kwargs)
        self.group.choices = [(None, None)] + [(str(group.id), group.name) for group in Interest_Group.query.all()]

class UpdateActivityFormClient(FlaskForm, ActivityMixin):
    image  = FileField("Activity Image")
    submit = SubmitField("Create Activity")

    def __init__(self, *args, **kwargs):
        super(UpdateActivityFormClient, self).__init__(*args, **kwargs)
        groups = Interest_Group.query.join(Membership, Membership.group_id == Interest_Group.id)\
            .filter(Membership.level == 1 or Membership.level == 2).all()
        self.group.choices = [(str(group.id), group.name) for group in groups]

class GroupMembershipForm(FlaskForm):
    join_group  = SubmitField("Join Group")
    leave_group = SubmitField("Leave Group")

class PerkFormMixin():
    title       = StringField("Perk Title")
    description = StringField("Perk Description", widget=TextArea())

class CreatePerkForm(FlaskForm, PerkFormMixin):
    image  = FileField("Perk Image", validators=[FileRequired()])
    submit = SubmitField("Create Perk")

class UpdatePerkForm(FlaskForm, PerkFormMixin):
    image  = FileField("Perk Image")
    submit = SubmitField("Update Perk")

class CreatePointRuleForm(FlaskForm, PerkFormMixin):
    name  = StringField("Pointing Rule Name")
    value = StringField("Value")
    submit = SubmitField("Submit")



