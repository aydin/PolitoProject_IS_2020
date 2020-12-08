from datetime import datetime
from FlaskBlog import db, login_manager
from flask_login import UserMixin, current_user


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

ACCESS = {
    'role1': 'user',
    'role2': 'producer'
}

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(15), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return "User(%r, %r, %r)" % (self.username, self.email, self.image_file)

    def is_Producer(self):
        return self.role == ACCESS['role2']

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Post(%r, %r)" % (self.title, self.date_posted)

