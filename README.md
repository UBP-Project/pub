# Unionbank Pub

### Project Setup

Install the requirements listed in requirements.txt

```sh
$ pip install -r requirements.txt
```

Configure database on config.py

```sh
SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    'mysql+pymysql://root:@localhost/pub_dev'
```
Create the tables by executing
```sh
$ python manage.py shell
>>> db.create_all() 
```

### Development

Run the development server
```sh
$ python manage.py runserver
```

### API
Access API's example (Todo API documentation)
```sh
https://[host]/api/v1.0/interest_groups/
```