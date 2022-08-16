from flask import render_template, url_for, flash, redirect, Blueprint, request
from flask_login import login_required, current_user

# App imports
from declutter.blueprints.users.account.forms.update_account import UpdateEmail, UpdatePassword, UpdateUsername
from declutter.blueprints.users.account.utilities.mailing import send_email_verification_request
from declutter.utilities.backend import db, bcrypt
from declutter.utilities.datetime import datetime_tolocal

# Database models
from declutter.models.users import Users


users_account = Blueprint(
    name = 'users_account', import_name = __name__,
    template_folder = '../../../templates/users/account', static_folder = '../../static')


@users_account.route("/account")
@login_required
def account():
    return render_template('account.html', title = 'Account', datetime_tolocal = datetime_tolocal)


@users_account.route("/update_username", methods = ['GET', 'POST'])
@login_required
def update_username():
    update_username_form = UpdateUsername()
    if update_username_form.validate_on_submit():
        current_user.user_username = update_username_form.user_username.data
        db.session.commit()
        flash('Username successfully updated!', 'success')
        return redirect(url_for('users_account.account'))

    return render_template('update_username.html', title = 'Username update', form = update_username_form)
    

@users_account.route("/update_password", methods = ['GET', 'POST'])
@login_required
def update_password():
    update_password_form = UpdatePassword()
    if update_password_form.validate_on_submit():
        current_user.user_password = (
            bcrypt
            .generate_password_hash(password = update_password_form.user_password_new_confirm.data)
            .decode('utf-8'))

        db.session.commit()
        flash('Password changed successfully!', 'success')
        return redirect(url_for('users_account.account'))

    return render_template('update_password.html', title = 'Password update', form = update_password_form)


@users_account.route("/update_email", methods = ['GET', 'POST'])
@login_required
def update_email():
    update_email_form = UpdateEmail()
    if update_email_form.validate_on_submit():
        current_user.user_email = update_email_form.user_email.data
        current_user.user_email_isverified = False
        db.session.commit()
        flash('Email updated successfully!', 'success')
        return redirect(url_for('users_account.account'))

    return render_template('update_email.html', title = 'Email update', form = update_email_form)


@users_account.route("/verify_email", methods = ['GET', 'POST'])
@login_required
def verify_email():
    if current_user.user_email_isverified:
        return redirect(url_for('users_account.account'))

    send_email_verification_request(current_user)

    flash('A link for email verification has been sent to your email', 'info')
    return redirect(url_for('users_account.account'))


@users_account.route("/email_verification<token>", methods = ['GET', 'POST'])
def email_verification(token):
    user = Users.verify_token(token)
    if user is None:
        flash('That is an invalid or or an expired token!', 'warning')
        return redirect(url_for('users_account.account'))

    user.user_email_isverified = True
    db.session.commit()

    flash('Email has been successfully verified', 'success')
    return redirect(url_for('users_account.account'))