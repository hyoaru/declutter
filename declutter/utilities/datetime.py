import pytz
from datetime import datetime, tzinfo
from dateutil import tz

def datetime_tolocal(datetime_utc):
    """Converts datetime utc to local datetime."""
    
    local_datetime = (
        datetime_utc
        .replace(tzinfo = pytz.UTC)
        .astimezone(tz.tzlocal())
    )

    return local_datetime