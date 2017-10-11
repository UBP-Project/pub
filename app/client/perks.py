import json
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from ..forms import LoginForm
from . import client
from app import db
from app.models import Perks
from ..auth import is_manager_or_leader
from ..forms import CreatePerkForm, UpdatePerkForm


@client.route('/perks/')
@login_required
def perks():
    return render_template("client/perks/perks.html", is_manager=is_manager())


@client.route('/perks/create', methods=['GET', 'POST'])
@login_required
def create_perks():
    form = CreatePerkForm()
    if form.validate_on_submit():
        perk = Perks(
            title=form.title.data,
            description=form.description.data
        )
        db.session.add(perk)
        db.session.commit()
        db.session.refresh(perk)
        perk.set_image(form.image.data)
        return redirect(url_for("client.perks"))
    return render_template("client/perks/create.html", form=form)


@client.route('/perks/<string:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_perk(id):
    form = UpdatePerkForm()
    perk = Perks.query.get_or_404(id)

    if request.method == 'POST' and request.form.get('delete') == 'delete':
        db.session.delete(perk)
        return redirect(url_for('client.perks'))

    if form.validate_on_submit():
        if form.image.data:
            perk.set_image(form.image.data)
        perk.title = form.title.data
        perk.description = form.description.data
        db.session.commit()
        return redirect(url_for("client.perks"))
    # load activity data to the form
    form.title.data = perk.title
    form.description.data = perk.description
    return render_template('client/perks/edit.html', form=form, perk=perk)
