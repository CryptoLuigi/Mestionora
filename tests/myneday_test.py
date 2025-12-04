import datetime
import pytz
import pytest

from src.extensions.misc import compute_myneday_state, MYNEDAY_TZ as tz


myne_hour = 16

start_dt = tz.localize(datetime.datetime(2025, 12, 15, myne_hour))
end_dt = tz.localize(datetime.datetime(2026, 3, 9, myne_hour))


test_cases = [
    {
        "name": "before_start_date",
        "now": tz.localize(datetime.datetime(2025, 11, 20, 10)),
        "want_state": "scheduled",
        "want_mynetime": start_dt,
    },
    {
        "name": "exact_start_monday_16",
        "now": tz.localize(datetime.datetime(2025, 12, 15, 16)),
        "want_state": "now",
        "want_mynetime": start_dt,
    },
    {
        "name": "monday_before_mynetime",
        "now": tz.localize(datetime.datetime(2025, 12, 15, 10)),
        "want_state": "now",
        "want_mynetime": start_dt,
    },
    {
        "name": "monday_after_mynetime_treated_as_now",
        "now": tz.localize(datetime.datetime(2025, 12, 15, 18)),
        "want_state": "now",
        "want_mynetime": start_dt,
    },
    {
        "name": "wednesday_between_start_end",
        "now": tz.localize(datetime.datetime(2025, 12, 17, 12)),  # Wednesday
        "want_state": "scheduled",
        "want_mynetime": tz.localize(
            datetime.datetime(2025, 12, 22, 16)
        ),  # next Monday
    },
    {
        "name": "regular_monday_after_start",
        "now": tz.localize(datetime.datetime(2025, 12, 22, 12)),  # Monday
        "want_state": "now",
        "want_mynetime": tz.localize(datetime.datetime(2025, 12, 22, 16)),
    },
    {
        "name": "just_before_end_date",
        "now": tz.localize(datetime.datetime(2026, 3, 9, 10)),
        "want_state": "now",
        "want_mynetime": end_dt,
    },
    {
        "name": "after_end_date",
        "now": tz.localize(datetime.datetime(2026, 3, 20, 10)),
        "want_state": "ended",
        "want_mynetime": end_dt,
    },
]


# ------------------------------
# Pytest table runner
# ------------------------------
@pytest.mark.parametrize("tc", test_cases, ids=[tc["name"] for tc in test_cases])
def test_myneday(tc):
    state, mynetime = compute_myneday_state(tc["now"], start_dt, end_dt)

    assert state == tc["want_state"], f"{tc['name']} wrong state"
    assert mynetime == tc["want_mynetime"], f"{tc['name']} wrong time"
