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
>>> Role.insert_roles()
```

Drop the Tables
```sh
$ python manage.py shell
>>> db.drop_all() 
```

### Create Administrator
```sh
$ python manage.py shell
>>> email = '<admin email>'
>>> password = '<password>'
>>> admin = User(email=email, password=password, role_id=3)
>>> db.session.add(admin)
>>> db.session.commit()
```

### Development

Run the development server
```sh
$ python manage.py runserver
```

### API
Access API's documentation
```sh
https://[host]/apidocs
```