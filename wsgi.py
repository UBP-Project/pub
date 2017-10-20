import os
from manage import app

os.environ["FLASK_CONFIG"] = "production"

if __name__ == "__main__":
	app.run()