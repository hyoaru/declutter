from flask import render_template, url_for, redirect, request, Blueprint

# App imports
from declutter.utilities.datetime import datetime_tolocal

# Database models
from declutter.models.posts import Posts


main = Blueprint(
    name = 'main', import_name = __name__,
    template_folder = '../../templates/main', static_folder = '../../static')


@main.route("/")
@main.route("/home", methods = ['GET', 'POST'])
def home():
    posts = (
        Posts.query
        .filter_by(post_isdeleted = False)
        .order_by(Posts.post_date_created_utc.desc())
        .paginate(per_page = 5, page = request.args.get(key = 'page', default = 1, type = int)))

    return render_template('home.html', posts = posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')