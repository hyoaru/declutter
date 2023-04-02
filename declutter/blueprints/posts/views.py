from flask import abort, render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_required, current_user

# App imports
from declutter.blueprints.posts.forms.post import PostCreate
from declutter.utilities.backend import db
from declutter.utilities.datetime import datetime_tolocal

# Database models
from declutter.models.posts import Posts


posts = Blueprint(
    name = 'posts_general', import_name = __name__,
    template_folder = '../../templates/posts', static_folder = '../../static')


@posts.route("/post/write", methods = ['GET', 'POST'])
@login_required
def post_create():
    post_create_form = PostCreate()
    if post_create_form.validate_on_submit():
        post = Posts(
            post_title = post_create_form.post_title.data,
            post_content = post_create_form.post_content.data,
            post_author = current_user, )

        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))

    return render_template('post_create.html', title = 'Write', form = post_create_form)


@posts.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = Posts.query.get_or_404(post_id)
    post_author_deleted_or_deactivated = post.post_author.user_isdeleted or post.post_author.user_isdeactivated
    if post.post_isdeleted or post_author_deleted_or_deactivated:
        abort(404)
    else:
        return render_template('post.html', title = post.post_title, post = post, )


@posts.route("/post/<int:post_id>/delete", methods = ['POST'])
def post_delete(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.post_author != current_user:
        abort(403)
    else:
        post.post_isdeleted = True
        # db.session.delete(post)
        db.session.commit()
        flash('Your post has been deleted!', 'success')
        return redirect(request.referrer)
