from tacview_timesync import tvts
from datetime import datetime, timedelta


def test_get_new_timestamp():
    result = tvts.get_new_timestamp(
        track_event_time=datetime.fromisoformat("2016-06-22T02:45:00Z") + timedelta(seconds=10),
        video_event_delta=timedelta(seconds=20),
    ).strftime("%Y%m%dT%H%M%SZ")
    assert result == "20160622T024450Z"
