from flask import render_template, url_for, redirect, request, Blueprint, abort
from flask_login import login_required, current_user

# App imports
from declutter.utilities.datetime import datetime_tolocal
from declutter.utilities.backend import db
from declutter.config import Config

# Database models
from declutter.models.users import Users
from declutter.models.posts import Posts

post_per_page = Config.POST_PER_PAGE

users_general = Blueprint(
    name = 'users_general', import_name = __name__,
    template_folder = '../../../templates/users/general', static_folder = '../../static')


@users_general.route("/profile")
@login_required
def profile():
    posts = (
        Posts.query
        .filter_by(post_user_id = current_user.user_id, post_isdeleted = False)
        .order_by(Posts.post_date_created_utc.desc())
        .paginate(per_page = post_per_page, page = request.args.get(key = 'page', default = 1, type = int)))
        
    return render_template('profile.html', title = 'Profile', posts = posts, post_count = posts.total, )


@users_general.route("/user/<user_username>")
@login_required
def user(user_username):
    user = (
        Users.query
        .filter_by(user_username = user_username)
        .first_or_404())

    if user != current_user:
        if user.user_isdeleted == True or user.user_isdeactivated == True:
            abort(404)
        else:
            posts = (
                Posts.query
                .filter_by(post_author = user, post_isdeleted = False)
                .order_by(Posts.post_date_created_utc.desc())
                .paginate(per_page = post_per_page, page = request.args.get(key = 'page', default = 1, type = int)))

            return render_template(
                'user.html', title = user.user_username, user = user, 
                posts = posts, post_count = posts.total)

    else:
        return redirect(url_for('users_general.profile'))