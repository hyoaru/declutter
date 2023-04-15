from datetime import datetime
from flask import request

# App imports
from declutter import create_app
from declutter.utilities.datetime import datetime_tolocal
from declutter.utilities.sidebar_elements import get_posts_recent_n, get_users_recent_n, get_daily_random_quotes

app = create_app()