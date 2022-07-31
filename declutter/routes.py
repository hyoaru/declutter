from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required, login_user, current_user, logout_user
from declutter import app
from declutter.blueprints.authentication.auth_register import RegistrationForm
from declutter.blueprints.authentication.auth_login import LoginForm
from declutter.database import db, bcrypt

# Database models
from declutter.blueprints.models.users import Users
from declutter.blueprints.models.posts import Posts

postlist = [
    {
        'author': 'User',
        'title': 'Some thoughts ive been keeping for a while',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus iaculis metus vel ex fringilla ornare vitae eget elit. Suspendisse efficitur congue eros, et tempus arcu. Mauris mollis, lectus et vehicula pellentesque, nibh ex rutrum lorem, ut sagittis enim odio quis nulla. Sed vehicula egestas cursus. Ut commodo eleifend condimentum. Nullam aliquam nunc imperdiet, euismod dui sed, bibendum turpis. Mauris eros est, feugiat a consequat in, lobortis eget leo. Morbi eleifend erat diam, in dapibus metus viverra vel.',
        'date': 'July 16, 2022'
    },
    {
        'author': 'User',
        'title': 'Une hirondelle ne fait pas le printemps',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus iaculis metus vel ex fringilla ornare vitae eget elit. Suspendisse efficitur congue eros, et tempus arcu. Mauris mollis, lectus et vehicula pellentesque, nibh ex rutrum lorem, ut sagittis enim odio quis nulla. Sed vehicula egestas cursus. Ut commodo eleifend condimentum. Nullam aliquam nunc imperdiet, euismod dui sed, bibendum turpis. Mauris eros est, feugiat a consequat in, lobortis eget leo. Morbi eleifend erat diam, in dapibus metus viverra vel.',
        'date': 'July 16, 2022'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('main/home.html', posts=postlist)

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
            user_password = bcrypt.generate_password_hash(registration_form.user_password.data).decode('utf-8')
        )

        db.session.add(registered_user)
        db.session.commit()

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

@app.route("/account")
@login_required
def account():
    return render_template('auth/account.html', title = 'Account')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))