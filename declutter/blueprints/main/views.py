from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import login_required

# App imports
from declutter.utilities.datetime import datetime_tolocal
from declutter.config import Config

# Database models
from declutter.models.posts import Posts
from declutter.models.users import Users

post_per_page = Config.POST_PER_PAGE

main = Blueprint(
    name = 'main', import_name = __name__,
    template_folder = '../../templates/main', static_folder = '../../static')


@main.route("/")
@main.route("/home", methods = ['GET', 'POST'])
@login_required
def home():
    posts = (
        Posts.query
        .filter(
            Posts.post_author.has(Users.user_isdeactivated == False),
            Posts.post_author.has(Users.user_isdeleted == False),)
        .filter_by(post_isdeleted = False)
        .order_by(Posts.post_date_created_utc.desc())
        .paginate(per_page = post_per_page, page = request.args.get(key = 'page', default = 1, type = int)))

    return render_template('home.html', posts = posts)


@main.route("/about")
def about():
    return render_template('about.html', title = 'About')


@main.route("/search")
@login_required
def search():

    query_request = request.args.get(key = 'query', type = str)
    search_query = '' if query_request is None else query_request

    query_by_user = (
        Users.query
        .filter(Users.user_username.contains(search_query))
        .filter_by(user_isdeactivated = False, user_isdeleted = False)
        .paginate(per_page = post_per_page, page = request.args.get(key = 'by_user_page', default = 1, type = int)))

    query_by_post_title = (
        Posts.query
        .filter(
            Posts.post_title.contains(search_query),
            Posts.post_author.has(Users.user_isdeactivated == False),
            Posts.post_author.has(Users.user_isdeleted == False), )
        .filter_by(post_isdeleted = False)
        .paginate(per_page = post_per_page, page = request.args.get(key = 'by_post_title_page', default = 1, type = int)))

    query_by_post_content = (
        Posts.query
        .filter(
            Posts.post_content.contains(search_query),
            Posts.post_author.has(Users.user_isdeactivated == False),
            Posts.post_author.has(Users.user_isdeleted == False), )
        .filter_by(post_isdeleted = False)
        .paginate(per_page = post_per_page, page = request.args.get(key = 'by_post_content_page', default = 1, type = int)))

    total_items_matched = (
        len(query_by_user.items)
        + len(query_by_post_title.items)
        + len(query_by_post_content.items))

    return render_template(
        'search.html', title = 'Search', search_query = search_query, query_by_user = query_by_user, 
        query_by_post_title = query_by_post_title, query_by_post_content = query_by_post_content,
        total_items_matched = total_items_matched)