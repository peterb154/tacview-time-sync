import argparse
from datetime import datetime, timedelta
import logging
import xattr
import sys

logging.basicConfig(level=logging.INFO)


def get_new_timestamp(
    track_start_time: datetime, track_event_delta: timedelta, video_event_delta: timedelta
) -> datetime:
    logging.debug(f"track_start_time: {track_start_time}")
    logging.debug(f"track_event_delta: {track_event_delta}")
    logging.debug(f"video_event_delta: {video_event_delta}")
    video_start_time = track_start_time - (video_event_delta - track_event_delta)
    return video_start_time


def add_timestamp_metadata_to_file(file_path: str, time_stamp: str) -> None:
    key = "Media Created"
    logging.info(f"Adding metadata to file {file_path} - ['{key}': '{time_stamp}']")
    xattr.setxattr(file_path, key, str(time_stamp).encode("utf-8"))


def get_file_metadata(file_path: str) -> None:
    for item in xattr.listxattr(file_path):
        val = xattr.getxattr(file_path, item)
        logging.debug(f"file: {file_path}, key: {item} value: {val}")


def parse_args(args: list) -> argparse.ArgumentParser.parse_args:
    parser = argparse.ArgumentParser(
        description="Calculate new video start timestamp from track start time, track event delta and video event delta"
    )
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument(
        "-tt",
        "--track-event-time",
        required=True,
        help='Track absolute event time in ISO 8601 format (ex: "2010-10-01 10:00:00")',
    )
    parser.add_argument(
        "-td",
        "--track-event-delta",
        required=True,
        help='Track event time in minutes and seconds from track start (ex: "0:10")',
    )
    parser.add_argument(
        "-vd",
        "--video-event-delta",
        required=True,
        help='Video event time in minutes and seconds from video start (ex: "0:20")',
    )
    parser.add_argument("-vf", "--video-file_name", help="optional video file name to which we will add metadata")
    return parser.parse_args(args)


def main(args: list = None) -> None:
    if not args:
        args = sys.argv[1:]  # pragma: no cover
    args = parse_args(args)
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    new_video_start_time = get_new_timestamp(
        track_start_time=datetime.fromisoformat(args.track_event_time),
        track_event_delta=timedelta(
            minutes=int(args.track_event_delta.split(":")[0]), seconds=int(args.track_event_delta.split(":")[1])
        ),
        video_event_delta=timedelta(
            minutes=int(args.video_event_delta.split(":")[0]), seconds=int(args.video_event_delta.split(":")[1])
        ),
    ).strftime("%Y%m%dT%H%M%SZ")
    print(f"new video start timestamp: {new_video_start_time}")
    if args.video_file_name:
        add_timestamp_metadata_to_file(args.video_file_name, new_video_start_time)
        if args.verbose:
            get_file_metadata(file_path=args.video_file_name)


if __name__ == "__main__":
    main(args=sys.argv[1:])  # pragma: no cover
