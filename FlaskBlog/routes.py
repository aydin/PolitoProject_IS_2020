import os
import secrets
from PIL import Image
from flask import render_template, url_for, redirect, flash, request, abort
from FlaskBlog import app, db, bcrypt
from FlaskBlog.forms import RegistrationForm, LoginForm, RetailerProductsForm, UpdateAccountForm
from FlaskBlog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required



#this is my change
#this is my 2nd change
#this is my 3rd change



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

def save_picture(form_picture):

    fname, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = fname + f_ext
    picture_path = os.path.join(app.root_path, 'static/Pics', picture_fn)
    form_picture.save(picture_path)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))

    image_file = url_for('static', filename='Pics/' + current_user.image_file)
    return render_template('account.html', title= 'Account', image_file=image_file, form=form)



@app.route('/create_farm', methods=['GET','POST'])
@login_required
def create_farm():
    if not current_user.is_Producer():
        return redirect(url_for('home'))
    form = RetailerProductsForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
        post = Post(title=form.title.data, content=form.content.data, image_farm_file=picture_file, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('your farm products page has been created', 'success')
        image_farm_file = url_for('static', filename='Pics/' + picture_file)
        return redirect(url_for('home', image=image_farm_file))

    image_farm_file = url_for('static', filename='Pics/' + post.image_farm_file)
    return render_template('create_retailer.html', form=form, image=image_farm_file)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

