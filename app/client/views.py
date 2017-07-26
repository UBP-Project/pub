from flask import render_template
from . import client

@client.route('/')
def index():
	return render_template("index.html")

@client.route('/home/')
def viewHome():
	return render_template('views/home.html')

@client.route('/login/')
def viewLogin():
	return render_template('views/login.html')