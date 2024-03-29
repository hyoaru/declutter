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

admin = Blueprint(
    name = 'admin', import_name = __name__,
    template_folder = '../../templates/admin', static_folder = '../../static')

    
@admin.route("/admin/user/<user_username>/deleted_posts")
@login_required
def user_deleted_posts(user_username):
    user = (
        Users.query
        .filter_by(user_username = user_username)
        .first_or_404())
    
    if user == current_user:
        return redirect(url_for('admin.profile_deleted_posts'))
    
    if current_user.user_isadmin == False:
        abort(403)
    else:
        posts = (
            Posts.query
            .filter_by(post_author = user, post_isdeleted = True)
            .order_by(Posts.post_date_created_utc.desc())
            .paginate(per_page = post_per_page, page = request.args.get(key = 'page', default = 1, type = int)))
        
        return render_template(
            'user_deleted_posts.html', title = user.user_username, user = user, 
            posts = posts, post_count = posts.total)

@admin.route("/admin/profile/deleted_posts")
@login_required
def profile_deleted_posts():
    user = current_user
    
    if current_user.user_isadmin == False:
        abort(403)
    else:
        posts = (
            Posts.query
            .filter_by(post_author = user, post_isdeleted = True)
            .order_by(Posts.post_date_created_utc.desc())
            .paginate(per_page = post_per_page, page = request.args.get(key = 'page', default = 1, type = int)))

        return render_template(
            'profile_deleted_posts.html', title = user.user_username, user = user, 
            posts = posts, post_count = posts.total)
    
@admin.route("/admin/user/<user_username>/mute")
@login_required
def mute_user(user_username):
    user = (
        Users.query
        .filter_by(user_username = user_username)
        .first_or_404())
    
    if ((current_user.user_isadmin == False) or (user.user_isadmin)):
        abort(403)
    else:
        user.user_ismuted = True
        db.session.commit()

    return redirect(request.referrer)
    
@admin.route("/admin/user/<user_username>/unmute")
@login_required
def unmute_user(user_username):
    user = (
        Users.query
        .filter_by(user_username = user_username)
        .first_or_404())
    
    if ((current_user.user_isadmin == False) or (user.user_isadmin)):
        abort(403)
    else:
        user.user_ismuted = False
        db.session.commit()

    return redirect(request.referrer)
    
