from datetime import datetime, time, timedelta, timezone


def get_aoab_next_prepub_timestamp():
    now = datetime.now(tz=timezone.utc)
    new_date = now.date()
    new_date = new_date + timedelta((-new_date.weekday()) % 7)
    release_time = datetime.combine(new_date, time(21, 0, 0, 0, timezone.utc))
    delta = release_time - now
    days = delta.days
    h = delta.seconds // 3600
    m = (delta.seconds % 3600) // 60
    s = delta.seconds % 60
    return days, h, m, s
