from declutter import create_app
from declutter.utilities.datetime import datetime_tolocal
from declutter.utilities.sidebar_elements import get_posts_recent_10

if __name__ == "__main__":
    app = create_app()

    @app.context_processor
    def inject_sidebar_elements():
        return dict(datetime_tolocal = datetime_tolocal, sidebar_posts = get_posts_recent_10())

    app.run(debug=True)
 