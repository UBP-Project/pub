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

Run SEED Script
```sh
$ python manage.py shell
>>> seed() 
```
(!) SEED Script already contains Role, Admin, and Several User Accounts
(!) It also includes 4 Groups and 5 Activities for Testing

Admin
```sh
email: admin@unionbank.com
password: admin
```

User
```sh
email: test@test.com
password: 12345
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
