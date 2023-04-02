import os
import pickle
import requests
from typing import Type
from datetime import datetime, timedelta

# Database models
from declutter.models.posts import Posts
from declutter.models.users import Users


def get_posts_recent_n(n: int) -> Type[Posts]:
    """Returns the recent 10 posts."""

    posts = (
        Posts.query
        .filter(
            Posts.post_author.has(Users.user_isdeactivated == False),
            Posts.post_author.has(Users.user_isdeleted == False),)        
        .filter_by(post_isdeleted = False)
        .order_by(Posts.post_date_created_utc.desc())
        .limit(n).all())

    return posts


def get_users_recent_n(n: int) -> Type[Users]:
    """Returns the 10 recently joined users."""

    users = (
        Users.query
        .filter_by(user_isdeleted = False, user_isdeactivated = False)
        .order_by(Users.user_date_created_utc.desc())
        .limit(n).all())

    return users


def saveto_binary(obj_structure, file_name: str, data_root_path: str = None) -> None:
    """Saves an object structure to binary format."""

    data_root_path = 'declutter/data' if data_root_path is None else data_root_path

    if not os.path.exists(f'{data_root_path}'):
        os.mkdir(f'{data_root_path}')

    with open(f'{data_root_path}/{file_name}.bin', 'wb') as file:
        pickle.dump(obj_structure, file)


def load_binary(file_name: str, data_root_path: str = None):
    """Loads and returns a binary object structure."""

    data_root_path = 'declutter/data' if data_root_path is None else data_root_path

    if os.path.exists(f'{data_root_path}/{file_name}.bin'):
        file = open(f'{data_root_path}/{file_name}.bin', 'rb')
        obj_structure = pickle.load(file)
        file.close()

        return obj_structure

    else:
        return {}


def get_daily_random_quotes(api: str = "https://api.quotable.io/random?tags=famous-quotes") -> dict:
    """Returns daily quote from an api if the dateToReload value of the quote dictionary is greater than utc date now."""

    quote = load_binary(file_name = 'sidebar_daily_quote')

    quote_date_to_reload = quote.get('dateToReload')
    if quote_date_to_reload is not None and quote_date_to_reload > datetime.utcnow().date():
        return quote
    else:
        try:
            request = requests.get(api)
        except:
            return {}

        quote = request.json()[0] if type(request.json()) == type([]) else request.json()
        quote.update({'dateToReload': datetime.utcnow().date() + timedelta(days = 1)})
        saveto_binary(obj_structure = quote, file_name = 'sidebar_daily_quote')

        return quote