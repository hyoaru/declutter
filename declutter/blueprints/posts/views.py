from flask import abort, render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_required, current_user

# App imports
from declutter.blueprints.posts.forms.post import PostCreate
from declutter.utilities.backend import db
from declutter.utilities.datetime import datetime_tolocal

# Database models
from declutter.models.posts import Posts


posts = Blueprint(
    name = 'posts', import_name = __name__,
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
def post(post_id):
    posts = Posts.query.get_or_404(post_id)
    print(f'Route: post, Request url: {request.url}')

    return render_template('post.html', title = posts.post_title, post = posts, )


@posts.route("/post/<int:post_id>/delete", methods = ['POST'])
def post_delete(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.post_author != current_user:
        abort(403)

    else:
        db.session.delete(post)
        db.session.commit()
        flash('Your post has been deleted!', 'success')
        return redirect(request.referrer)
