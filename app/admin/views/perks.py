from .. import admin
from flask import render_template, redirect, url_for, request
from ...decorators import admin_required
from ...forms import CreatePerkForm, UpdatePerkForm
from werkzeug.utils import secure_filename
from app.models import Perks
import uuid
import os
from app import db
from sqlalchemy import or_

PERKS_PER_PAGE = 8

@admin.route('/perks')
@admin_required
def perks():
    page = 1
    if 'page' in request.args:
        page = int(request.args.get('page'))
        print("PAGE", page)
    query = None
    if 'query' in request.args:
        query = request.args.get('query');
        q = query.lower()
        perks = Perks.query.filter(or_(
                Perks.title.ilike("%"+q+"%"),
                Perks.description.ilike("%"+q+"%")
            )).order_by(Perks.timestamp.desc()).paginate(
            page=page, per_page=PERKS_PER_PAGE, error_out=False)
    else:
        perks = Perks.query.order_by(Perks.timestamp.desc()).paginate(
            page=page, per_page=PERKS_PER_PAGE, error_out=False)
    return render_template('admin/perk/perks.html', perks=perks, query=query)

@admin.route('/perks/create', methods=['GET', 'POST'])
@admin_required
def create_perk():
    form = CreatePerkForm()
    if form.validate_on_submit():
        image = form.image.data
        image_filename = secure_filename(image.filename)
        extension = image_filename.rsplit('.', 1)[1].lower()
        image_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
        file_path             = os.path.join('app/static/uploads/perks_images', image_hashed_filename)
        image.save(file_path)

        perk = Perks(
            title=form.title.data,
            description=form.description.data,
            image=image_hashed_filename
        )
        db.session.add(perk)
        db.session.commit()
        return redirect(url_for("admin.perks"))
    return render_template('admin/perk/create.html', form=form)

@admin.route('/perks/<string:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_perk(id):
    form = UpdatePerkForm()
    perk = Perks.query.get_or_404(id)

    if request.method == 'POST' and request.form.get('delete') == 'delete':
        db.session.delete(perk)
        return redirect(url_for('admin.perks'))

    if form.validate_on_submit():
        if form.image.data:
            image = form.image.data
            image_filename = secure_filename(image.filename)
            extension = image_filename.rsplit('.', 1)[1].lower()
            image_hashed_filename = str(uuid.uuid4().hex) + '.' + extension
            file_path             = os.path.join('app/static/uploads/perks_images', image_hashed_filename)
            image.save(file_path)
            perk.image = image_hashed_filename
        perk.title = form.title.data
        perk.description = form.description.data
        db.session.commit()
        return redirect(url_for("admin.perks"))
    # load activity data to the form
    form.title.data       = perk.title
    form.description.data = perk.description
    return render_template('admin/perk/edit.html', form=form, perk=perk)