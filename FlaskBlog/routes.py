import os
from flask import render_template, url_for, redirect, flash, request, abort
from FlaskBlog import app, db, bcrypt
from FlaskBlog.forms import RegistrationForm, LoginForm, RetailerProductsForm
from FlaskBlog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required



#this is my change

@app.route('/home')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route('/')
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Account is created, you can now Sign In!','success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash('You have been logged in!', 'success')
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login failed, Check credentials!', 'danger')
    return render_template('login.html', title='SignIn', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/create_farm', methods=['GET','POST'])
@login_required
def create_farm():
    if not current_user.is_Producer():
        return redirect(url_for('home'))
    form = RetailerProductsForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('your farm products page has been created','success')
        return redirect(url_for('home'))
    return render_template('create_retailer.html', form=form)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

