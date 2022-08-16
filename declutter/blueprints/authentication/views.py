from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user

# App imports
from declutter.blueprints.authentication.forms.register import RegistrationForm
from declutter.blueprints.authentication.forms.login import LoginForm
from declutter.blueprints.authentication.forms.forgot_password import ForgotPassword
from declutter.blueprints.authentication.forms.reset_password import ResetPassword
from declutter.blueprints.authentication.utilities.mailing import send_reset_password_email
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


@authentication.route("/forgot_password", methods = ['GET','POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    forgot_password_form = ForgotPassword()
    if forgot_password_form.validate_on_submit():
        user = (
            Users.query.filter_by(user_email = forgot_password_form.user_input.data).first()
            or Users.query.filter_by(user_username = forgot_password_form.user_input.data).first())
        
        send_reset_password_email(user)
        flash(f'A link for password reset has been sent to your email', 'info')
        return redirect(url_for('authentication.forgot_password'))

    return render_template('forgot_password.html', title = 'Forgot password', form = forgot_password_form)


@authentication.route("/reset_password/<reset_token>", methods = ['GET', 'POST'])
def reset_password(reset_token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = Users.verify_reset_token(reset_token)
    if user is None:
        flash('That is an invalid or an expired token!', 'warning')
        return redirect(url_for('authentication.forgot_password'))

    reset_password_form = ResetPassword()
    if reset_password_form.validate_on_submit():
        user.user_password = (
            bcrypt
            .generate_password_hash(reset_password_form.user_password_confirm.data)
            .decode('utf-8'))

        db.session.commit()
        flash(f'Your password has been updated!', 'success')
        return redirect(url_for('authentication.login'))

    return render_template('reset_password.html', title = 'Reset Password', form = reset_password_form)

    