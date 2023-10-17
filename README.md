# tacview-time-sync
This project aims to make it easier to synchronize tacview acmi tracks with recorded video files. 
It does this by calculating the new video start timestamp based on the track event time and the video event delta.

The resulting timestamp can be added to the video filename, or this script can modify the file to add the
timestamp as metadata.

See https://tacview.fandom.com/wiki/Synchronized_Audio/Video_Playback for more information.

# Requirements
- python3.6+

# Installation
`pip install tacview-timesync`

# Usage
```
$ tvts --help 
usage: tvts [-h] [-v] -tt TRACK_EVENT_TIME -vd VIDEO_EVENT_DELTA [-vf VIDEO_FILE_NAME]

Calculate new video start timestamp from track event time and video event delta

options:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -tt TRACK_EVENT_TIME, --track-event-time TRACK_EVENT_TIME
                        Track absolute event time in ISO 8601 format (ex: "2020-06-01 17:00:00")
  -vd VIDEO_EVENT_DELTA, --video-event-delta VIDEO_EVENT_DELTA
                        Video event time in minutes and seconds from video start (ex: "5:43")
  -vf VIDEO_FILE_NAME, --video-file_name VIDEO_FILE_NAME
                        optional video file name to which we will add metadata
```

# Examples

#### To get the correct timestamp for a video file:
1. Identify an event that you can see happen in the track file and in the video (i.e. start taxi)
2. Determine the absolute time of the event in the track file (i.e. 2020-06-01 17:00:00).
3. Then determine the offset time of the event in the video (i.e. 5:43 into the video).
4. Then run the following command to calculate the new video start timestamp:
    ```
    $ tvts -tt "2020-06-01 17:00:00" -vd "5:43"
    new video start timestamp: 20200601T165417Z
    ```
5. Add the new video start timestamp to the video file name (i.e. `sockeye-dcs-20200601T165417Z.mp4`)

#### To add the timestamp as metadata to a file, add the -vf argument:
```
$ tvts -tt "2020-06-01 17:00:00" -vd "5:43" -vf sockeye-dcs.mp4
new video start timestamp: 20200601T165417Z
INFO:root:Adding metadata to file sockeye-dcs.mp4 - ['Media Created': '20200601T165417Z']
```

# Developer Setup

## Requirements
- python3.6+
- poetry

## Setup
```
git clone <repo>
cd <repo>
poetry install
```
