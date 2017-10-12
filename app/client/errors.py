from flask import render_template, jsonify, request
from . import client

@client.app_errorhandler(400)
def bad_request_error(e):
    return render_template('error/400.html'),	400

@client.app_errorhandler(401)
def unathorized_error(e):
    return render_template('error/401.html'),	401

@client.app_errorhandler(403)
def forbidden_error(e):
    return render_template('error/403.html'),	403

@client.app_errorhandler(404)
def page_not_found(e):
	if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
		response = jsonify({'error': 'not found'})
		response.status_code = 404
		return response
	return render_template('error/404.html'),	404

@client.app_errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html'),	500

@client.app_errorhandler(503)
def service_unavailable_error(e):
    return render_template('error/503.html'),	503