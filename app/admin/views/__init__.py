from flask import render_template, flash
from .. import admin
from ...decorators import admin_required
from . import activities, groups, users

@admin.route('/', methods=['GET'])
@admin_required
def index():
    return render_template('admin_index.html');