from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
bootstrap = Bootstrap(app)

# Todo: Move the sql credentials to config.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/alchetest'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)


# Move the models to models.py
# Models
class Interest_Group(db.Model):
    __tablename__ = 'interest_group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, index=True)
    about = db.Column(db.String(1000))
    cover_photo = db.Column(db.String(500))
    group_icon = db.Column(db.String(100))

    def __repr__(self):
        return '<User %r>' % self.username


# Views
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)