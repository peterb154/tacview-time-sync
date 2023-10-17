from tacview_timesync import tvts
from datetime import datetime, timedelta
from unittest import mock

TEST_FILE_NAME = "test.mp4"


def test_get_new_timestamp_earlier():
    result = tvts.get_new_timestamp(
        track_start_time=datetime.fromisoformat("2020-01-10 10:00:00"),  # track starts at 10am
        track_event_delta=timedelta(seconds=10),  # event is 10 seconds into track
        video_event_delta=timedelta(seconds=20),  # event is 20 seconds into video
    ).strftime("%Y-%m-%d %H:%M:%S")
    assert result == "2020-01-10 09:59:50"  # video needs to start 10 seconds earlier than track


def test_get_new_timestamp_later():
    result = tvts.get_new_timestamp(
        track_start_time=datetime.fromisoformat("2020-01-10 10:00:00"),  # track starts at 10am
        track_event_delta=timedelta(seconds=20),  # event is 20 seconds into track
        video_event_delta=timedelta(seconds=10),  # event is 10 seconds into video
    ).strftime("%Y-%m-%d %H:%M:%S")
    assert result == "2020-01-10 10:00:10"  # video needs to start 10 seconds later than track


def test_get_new_timestamp_same():
    result = tvts.get_new_timestamp(
        track_start_time=datetime.fromisoformat("2020-01-10 10:00:00"),  # track starts at 10am
        track_event_delta=timedelta(seconds=10),  # event is 10 seconds into track
        video_event_delta=timedelta(seconds=10),  # event is 10 seconds into video
    ).strftime("%Y-%m-%d %H:%M:%S")
    assert result == "2020-01-10 10:00:00"  # video starts at same time as track


def test_parse_args():
    result = tvts.parse_args(
        args=["-tt", "2020-01-10 10:00:00", "-td", "0:10", "-vd", "0:20", "-vf", TEST_FILE_NAME, "-v"]
    )
    assert result.track_event_time == "2020-01-10 10:00:00"
    assert result.track_event_delta == "0:10"
    assert result.video_event_delta == "0:20"
    assert result.video_file_name == TEST_FILE_NAME
    assert result.verbose is True


def test_parse_args_terse():
    result = tvts.parse_args(
        args=["-tt", "2020-01-10 10:00:00", "-td", "0:10", "-vd", "0:20"]
    )
    assert result.track_event_time == "2020-01-10 10:00:00"
    assert result.track_event_delta == "0:10"
    assert result.video_event_delta == "0:20"
    assert result.video_file_name is None
    assert result.verbose is False


@mock.patch("tacview_timesync.tvts.xattr")
def test_get_file_metadata(mock_xattr):
    mock_xattr.listxattr.return_value = ["key1", "key2"]
    mock_xattr.getxattr.side_effect = ["value1", "value2"]
    tvts.get_file_metadata(file_path=TEST_FILE_NAME)
    mock_xattr.listxattr.assert_called_with(TEST_FILE_NAME)
    mock_xattr.getxattr.assert_any_call(TEST_FILE_NAME, "key1")
    mock_xattr.getxattr.assert_any_call(TEST_FILE_NAME, "key2")


@mock.patch("tacview_timesync.tvts.xattr")
def test_add_timestamp_metadata_to_file(mock_xattr):
    tvts.add_timestamp_metadata_to_file(file_path=TEST_FILE_NAME, time_stamp="20200101T000000Z")
    mock_xattr.setxattr.assert_called_with(TEST_FILE_NAME, "Media Created", b"20200101T000000Z")


@mock.patch("tacview_timesync.tvts.get_file_metadata")
@mock.patch("tacview_timesync.tvts.add_timestamp_metadata_to_file")
def test_main_file_verbose(mock_add_timestamp_metadata_to_file, mock_get_file_metadata):
    tvts.main(args=["-tt", "2020-01-10 10:00:00", "-td", "0:10", "-vd", "0:20", "-vf", TEST_FILE_NAME, "-v"])
    mock_get_file_metadata.assert_called_once_with(file_path=TEST_FILE_NAME)
    mock_add_timestamp_metadata_to_file.assert_called_once_with(TEST_FILE_NAME, "20200110T095950Z")


@mock.patch("tacview_timesync.tvts.get_file_metadata")
@mock.patch("tacview_timesync.tvts.add_timestamp_metadata_to_file")
def test_main_file_terse(mock_add_timestamp_metadata_to_file, mock_get_file_metadata):
    tvts.main(
        args=[
            "-tt",
            "2020-01-10 10:00:00",
            "-td",
            "0:10",
            "-vd",
            "0:20",
            "-vf",
            TEST_FILE_NAME,
        ]
    )
    mock_get_file_metadata.assert_not_called()
    mock_add_timestamp_metadata_to_file.assert_called_once_with(TEST_FILE_NAME, "20200110T095950Z")


@mock.patch("tacview_timesync.tvts.get_file_metadata")
@mock.patch("tacview_timesync.tvts.add_timestamp_metadata_to_file")
def test_main_terse(mock_add_timestamp_metadata_to_file, mock_get_file_metadata):
    tvts.main(
        args=[
            "-tt",
            "2020-01-10 10:00:00",
            "-td",
            "0:10",
            "-vd",
            "0:20",
        ]
    )
    mock_get_file_metadata.assert_not_called()
    mock_add_timestamp_metadata_to_file.assert_not_called()
