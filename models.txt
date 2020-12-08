from datetime import datetime
from FlaskBlog import db, login_manager
from flask_login import UserMixin, current_user


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    producers = db.relationship('Producer', backref='user', lazy='dynamic')

    def __repr__(self):
        return "User(%r, %r, %r)" % (self.username, self.email, self.image_file)

class Producer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    farmName = db.Column(db.String(30), unique=True, nullable=False)
    posts = db.relationship('Post', backref='producer', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "User(%r)" % (self.farmName)

class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    producer_id = db.Column(db.Integer, db.ForeignKey('producer.id'), nullable=False)

    def __repr__(self):
        return "Post(%r, %r)" % (self.title, self.date_posted)










