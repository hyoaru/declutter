from declutter import app
from declutter.blueprints.forms.authentication.auth_register import RegistrationForm
from declutter.blueprints.forms.authentication.auth_login import LoginForm
from declutter.blueprints.forms.authentication.auth_update_account import UpdateEmail, UpdatePassword, UpdateUsername
from declutter.blueprints.forms.main.post import PostCreate
from declutter.database import db, bcrypt
from declutter.blueprints.modules.datetime import datetime_tolocal

from flask import abort, render_template, url_for, flash, redirect, request
from flask_login import login_required, login_user, current_user, logout_user

# Database models
from declutter.blueprints.models.users import Users
from declutter.blueprints.models.posts import Posts

@app.route("/")
@app.route("/home")
def home():
    posts = Posts.query.all()
    return render_template('main/home.html', posts = posts, datetime_tolocal = datetime_tolocal)

@app.route("/about")
def about():
    return render_template('main/about.html', title='About')

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        registered_user = Users(
            user_email = registration_form.user_email.data,
            user_username = registration_form.user_username.data,
            user_password = bcrypt.generate_password_hash(registration_form.user_password_confirm.data).decode('utf-8')
        )
        db.session.add(registered_user)
        db.session.commit()
        login_user(user = Users.query.filter_by(user_email = registered_user.user_email).first())
        flash(f'Account successfully created for {registration_form.user_username.data}!', 'success')
        return redirect(url_for('login'))

    return render_template('auth/register.html', title = 'Register', form = registration_form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = Users.query.filter_by(user_username = login_form.user_username.data).first()
        if user and bcrypt.check_password_hash(pw_hash = user.user_password, password = login_form.user_password.data):
            login_user(user = user, remember = login_form.login_remember.data)
            flash(f'You have successfully logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful! Please check username and password.', 'danger')
    return render_template('auth/login.html', title = 'Login', form = login_form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('auth/account.html', title = 'Account', datetime_tolocal = datetime_tolocal)

@app.route("/update_username", methods = ['GET', 'POST'])
@login_required
def update_username():
    update_username_form = UpdateUsername()
    if update_username_form.validate_on_submit():
        current_user.user_username = update_username_form.user_username.data
        db.session.commit()
        flash('Username successfully updated!', 'success')
        return redirect(url_for('account'))
    return render_template('auth/update_username.html', title = 'Username update', form = update_username_form)
    
@app.route("/update_password", methods = ['GET', 'POST'])
@login_required
def update_password():
    update_password_form = UpdatePassword()
    if update_password_form.validate_on_submit():
        current_user.user_password = bcrypt.generate_password_hash(password = update_password_form.user_password_new_confirm.data).decode('utf-8')
        db.session.commit()
        flash('Password changed successfully!', 'success')
        return redirect(url_for('account'))
    return render_template('auth/update_password.html', title = 'Password update', form = update_password_form)

@app.route("/update_email", methods = ['GET', 'POST'])
@login_required
def update_email():
    update_email_form = UpdateEmail()
    if update_email_form.validate_on_submit():
        current_user.user_email = update_email_form.user_email.data
        db.session.commit()
        flash('Email updated successfully!', 'success')
        return redirect(url_for('account'))
    return render_template('auth/update_email.html', title = 'Email update', form = update_email_form)

@app.route("/post/write", methods = ['GET', 'POST'])
@login_required
def post_create():
    post_create_form = PostCreate()
    if post_create_form.validate_on_submit():
        post = Posts(
            post_title = post_create_form.post_title.data,
            post_content = post_create_form.post_content.data,
            post_author = current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('main/post_create.html', title = 'Write', form = post_create_form)

@app.route("/post/<int:post_id>")
def post(post_id):
    posts = Posts.query.get_or_404(post_id)
    print(f'Route: post, Request url: {request.url}')
    return render_template('main/post.html', title = posts.post_title, post = posts, datetime_tolocal = datetime_tolocal)

@app.route("/profile")
@login_required
def profile():
    posts = Posts.query.filter_by(post_user_id = current_user.user_id).all()
    return render_template('main/profile.html', title = 'Profile', posts = posts, post_count = len(posts), datetime_tolocal = datetime_tolocal)

@app.route("/user/<user_username>")
@login_required
def user(user_username):
    user = Users.query.filter_by(user_username = user_username).first_or_404()
    if user != current_user:
        posts = Posts.query.filter_by(post_author = user).all()
        return render_template('main/user.html', title = user.user_username, user = user, posts = posts, post_count = len(posts), datetime_tolocal = datetime_tolocal)
    else:
        return redirect(url_for('profile'))

@app.route("/post/<int:post_id>/delete", methods = ['POST'])
def post_delete(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.post_author != current_user:
        abort(403)
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Your post has been deleted!', 'success')
        return redirect(request.referrer)
