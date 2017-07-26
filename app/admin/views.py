from flask import render_template
from . import admin
from .forms import CreateUserForm
from app import db
from ..models import User

@admin.route('/', methods=['GET', 'POST'])
def index():
    create_user_form = CreateUserForm()
    print(create_user_form.validate_on_submit())
    if create_user_form.validate_on_submit():
        print("Creating User")
        user = User(firstname=create_user_form.firstname.data, 
            email=create_user_form.email.data)
        user.password = create_user_form.password.data
        db.session.add(user)
        db.session.commit()
    return render_template('admin/index.html',
                    create_user_form=create_user_form);
