from flask import render_template, flash
from .. import admin

from . import activities, groups, users

@admin.route('/', methods=['GET'])
def index():
    return render_template('admin_index.html');