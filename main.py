from datetime import datetime, timedelta


def get_new_timestamp(
        track_start_time: datetime,
        track_event_delta: timedelta,
        video_start_time: datetime,
        video_event_delta: timedelta) -> datetime:
    track_event_time = track_start_time + track_event_delta
    video_event_time = video_start_time + video_event_delta
    diff = track_event_time - video_event_time
    return video_start_time + diff


if __name__ == "__main__":
    new_video_start_time = get_new_timestamp(
        track_start_time=datetime.fromisoformat("2016-06-22T02:45:00Z"),
        track_event_delta=timedelta(seconds=10),
        video_start_time=datetime.fromisoformat("20231015T170250Z"),
        video_event_delta=timedelta(seconds=20)
    ).strftime("%Y%m%dT%H%M%SZ")
    print(new_video_start_time)