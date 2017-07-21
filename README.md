
pip install -r requirements.txt

To Setup the Database, edit the config.py then run

>>> python manage.py shell
>>> db.create_all()

To Run the server
>>> python manage.py runserver