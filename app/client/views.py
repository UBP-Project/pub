from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, logout_user
from .forms import LoginForm
from . import client
from ..models import User, Interest_Group

@client.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html");

@client.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not  None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('client.index'))
    return render_template("login.html", form=form)

@client.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("client.login"))