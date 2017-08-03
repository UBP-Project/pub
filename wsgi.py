from app import create_app

if __name__ == "__main__":
	app = create_app(os.getenv('FLASK_CONFIG') or 'default')
	app.run()