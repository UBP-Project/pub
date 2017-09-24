from flask import render_template, redirect, url_for, request
from .. import admin
from app import db
from app.models import Points_Type, Points, User
from ...decorators import admin_required
from app.forms import CreatePointRuleForm

@admin.route('/points', methods=['GET','POST'])
@admin_required
def points():
	form = CreatePointRuleForm()

	if request.method == 'POST':
		name = form.name.data
		value = form.value.data

		type = Points_Type(name, value)

		db.session.add(type)
		db.session.commit()

		return redirect(url_for("admin.points"))

	return render_template('admin/points/points.html', form=form)

