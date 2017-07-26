from flask import render_template
from . import main

@admin.route('/', methods=['GET', 'POST'])
def index():
    return "Admin page";
