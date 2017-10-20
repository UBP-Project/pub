import os
from manage import app

os.environ["FLASK_CONFIG"] = "production"

if __name__ == "__main__":
	app.run()


#import os
#from app import create_app

#if __name__ == "__main__":
#    app = create_app(os.getenv('FLASK_CONFIG') or 'production')
#    app.run()
