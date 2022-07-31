from flask import render_template, url_for, flash, redirect
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
    return render_template('blog/home.html', posts=postlist)

@app.route("/about")
def about():
    return render_template('blog/about.html', title='About')

@app.route("/register", methods = ['GET', 'POST'])
def register():
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
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if login_form.user_username.data == 'hyo' and login_form.user_password.data == '12345678':
            flash(f'You have successfully logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful! Please check username and password.', 'warning')
    return render_template('auth/login.html', title = 'Login', form = login_form)
