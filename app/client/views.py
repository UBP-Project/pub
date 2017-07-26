from flask import render_template
from . import client

@client.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html");
