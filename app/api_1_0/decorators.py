
from threading import Thread
from functools import wraps
from flask import abort
from flask_login import current_user
from app.models import Notification

def run_async(f):
	def async_func(*args, **kwwargs):
		func = Thread(target=f, args=args, kwargs=kwargs)
		func.start()
		return func
	return async_func

def follow_notif(f):
	def wrapper(*args, **kwargs):
		#pre process here
		
		#function
		output = f(*args, **kwargs)

		#async function to create notifications
		@run_async
		def push_notifications(*args, **kwargs):
			print(args)
			print(kwargs)
		
		return output
	return wrapper

