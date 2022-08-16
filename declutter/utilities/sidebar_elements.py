from typing import Type

# Database models
from declutter.models.posts import Posts
from declutter.models.users import Users


def get_posts_recent_10() -> Type[Posts]:
    posts = (
        Posts.query
        .order_by(Posts.post_date_created_utc.desc())
        .limit(10).all())

    return posts