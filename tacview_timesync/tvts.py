import argparse
from datetime import datetime, timedelta
import logging
import xattr

logging.basicConfig(level=logging.INFO)


def get_new_timestamp(track_event_time: datetime, video_event_delta: timedelta) -> datetime:
    logging.debug(f"track_event_time: {track_event_time}")
    logging.debug(f"video_event_delta: {video_event_delta}")
    video_start_time = track_event_time - video_event_delta
    return video_start_time


def add_timestamp_metadata_to_file(file_path: str, time_stamp: datetime) -> None:
    key = "Media Created"
    logging.info(f"Adding metadata to file {file_path} - ['{key}': '{time_stamp}']")
    xattr.setxattr(file_path, key, str(time_stamp).encode("utf-8"))


def get_file_metadata(file_path: str) -> None:
    for item in xattr.listxattr(file_path):
        val = xattr.getxattr(file_path, item)
        logging.debug(f"file: {file_path}, key: {item} value: {val}")


def parse_args() -> argparse.ArgumentParser.parse_args:
    parser = argparse.ArgumentParser(
        description="Calculate new video start timestamp from track event time and video event delta"
    )
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument(
        "-tt",
        "--track-event-time",
        required=True,
        help='Track absolute event time in ISO 8601 format (ex: "2020-06-01 17:00:00")',
    )
    parser.add_argument(
        "-vd",
        "--video-event-delta",
        required=True,
        help='Video event time in minutes and seconds from video start (ex: "5:43")',
    )
    parser.add_argument("-vf", "--video-file_name", help="optional video file name to which we will add metadata")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    v_minutes = int(args.video_event_delta.split(":")[0])
    v_seconds = int(args.video_event_delta.split(":")[1])
    new_video_start_time = get_new_timestamp(
        track_event_time=datetime.fromisoformat(args.track_event_time),
        video_event_delta=timedelta(minutes=v_minutes, seconds=v_seconds),
    ).strftime("%Y%m%dT%H%M%SZ")
    print(f"new video start timestamp: {new_video_start_time}")
    if args.video_file_name:
        add_timestamp_metadata_to_file(args.video_file_name, new_video_start_time)
        if args.verbose:
            get_file_metadata(file_path=args.video_file_name)


if __name__ == "__main__":
    main()
