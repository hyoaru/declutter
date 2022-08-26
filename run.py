from datetime import datetime
from flask import request

# App imports
from declutter import create_app
from declutter.utilities.datetime import datetime_tolocal
from declutter.utilities.sidebar_elements import get_posts_recent_10, get_users_recent_10, get_daily_random_quotes

if __name__ == "__main__":
    app = create_app()

    @app.context_processor
    def inject_global_elements():
        return dict(
            datetime_tolocal = datetime_tolocal, datetime_utcnow = datetime.utcnow(), 
            posts_recent_10 = get_posts_recent_10(), users_recent_10 = get_users_recent_10(), 
            quote_of_the_day = get_daily_random_quotes(), request = request)

    app.run(debug=True)
 