from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user

# App imports
from declutter.blueprints.authentication.forms.register import RegistrationForm
from declutter.blueprints.authentication.forms.login import LoginForm
from declutter.utilities.backend import db, bcrypt

# Database models
from declutter.models.users import Users


authentication = Blueprint(
    name = 'authentication', import_name = __name__,
    template_folder = '../../templates/authentication', static_folder = '../../static')


@authentication.route("/register", methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        registered_user = Users(
            user_email = registration_form.user_email.data,
            user_username = registration_form.user_username.data,
            user_password = (
                bcrypt
                .generate_password_hash(registration_form.user_password_confirm.data)
                .decode('utf-8')),)

        db.session.add(registered_user)
        db.session.commit()
        login_user(user = Users.query.filter_by(user_email = registered_user.user_email).first())
        flash(f'Account successfully created for {registration_form.user_username.data}!', 'success')
        return redirect(url_for('authentication.login'))

    return render_template('register.html', title = 'Register', form = registration_form)


@authentication.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = Users.query.filter_by(user_username = login_form.user_username.data).first()
        if user and bcrypt.check_password_hash(pw_hash = user.user_password, password = login_form.user_password.data):
            login_user(user = user, remember = login_form.login_remember.data)
            flash(f'You have successfully logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))

        else:
            flash('Login unsuccessful! Please check username and password.', 'danger')

    return render_template('login.html', title = 'Login', form = login_form)


@authentication.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))