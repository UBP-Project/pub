from flask import render_template, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from ..forms import LoginForm
from . import client
from app import db
from app.models import User, Follow, Points
from sqlalchemy.sql import func


@client.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template("client/index.html", user=current_user)


EMAIL_DOMAIN = 'unionbank.com'


@client.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    hasError = False
    if form.validate_on_submit():
        email = form.email.data
        if '@' not in email:  # allows login of emails with @unionbank.com
            email = email + '@' + EMAIL_DOMAIN
        user = User.query.filter_by(email=email).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            if(user.is_administrator()):
                return redirect(url_for('admin.index'))
            else:
                return redirect(request.args.get('next') or url_for('client.index'))
        hasError = True
    return render_template("client/views/login.html", form=form, hasError=hasError)


@client.route('/notifications/')
@login_required
def notifications():
    return render_template("client/views/notifications.html")


@client.route('/leaderboard')
@login_required
def leaderboard():

    point_leaders = db.session.query(Points, func.sum(Points.value).label('points'))\
        .join(User)\
        .group_by(Points.user_id)\
        .add_columns(User.id, User.firstname, User.lastname, User.image)\
        .order_by('points DESC')\
        .limit(10)\
        .all()

    followed_leaders = db.session.query(Follow,
            func.count(Follow.following_id).label('total'), Follow.following_id)\
        .join(User, User.id == Follow.following_id)\
        .add_columns(User.id, User.firstname, User.lastname, User.image)\
        .group_by(Follow.following_id).order_by('total DESC').limit(10).all()

    return render_template("client/views/leaderboard.html", user=current_user,
                           point_leaders=point_leaders,
                           followed_leaders=followed_leaders)


@client.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("client.login"))


@client.route('/search', methods=['GET'])
@login_required
def search():
    return render_template('client/views/search.html')
