# tacview-time-sync
This project aims to make it easier to synchronize tacview acmi tracks with recorded video files. 
It does this by calculating the correct video start timestamp relative to the track file.

The resulting video start timestamp can be added to the video filename, or this script can modify the file to add the
timestamp as metadata. See https://tacview.fandom.com/wiki/Synchronized_Audio/Video_Playback for more information.

The goal is to determine the correct start time for the video, so that it aligns with the track. 
- In the illustration below, the tacview track file starts at 2020-10-01 at 10:00 am. This is the "tt" or track time
expressed in ISO 8601 format. ex: "2020-10-10 10:00:00"
- At 10 seconds after the track starts, an event occurs, perhaps a jet starts to taxi. This is the "td" or track delta
expressed in minutes:seconds. ex: "0:10"
- At 20 seconds after the video starts, the same event occurs. This is the "vd" or video delta expressed in 
minutes:seconds. ex: "0:20". The reason for the difference is that tracks and videos rarely start at the same time,
but tacview needs to know how to align the 2 files. 
- To tell tacview when to start the video in reference to the track, we can include the video start timestamp in the
filename or in the file metadata.

```
       tt = track start time, assume 2020-10-10 10:00:00 (this is the dcs mission time)
       |______________________________|
       |             td               |  << track file
       |______________________________|     track delta (td) the time into the track where the event occurs
    |____________________________________|
    |                vd                  |  << video file, usually starts before and ends after track
    |____________________________________|     video delta (vd) is the time into the video where the same event occurs
                     ^ = event delta, an event, like starting to taxi where you can see it in the track and video
```


# Requirements
- python3.6+

# Installation
`pip install tacview-timesync`

# Usage
```
$ tvts -h
usage: tvts [-h] [-v] -tt TRACK_EVENT_TIME -td TRACK_EVENT_DELTA -vd VIDEO_EVENT_DELTA [-vf VIDEO_FILE_NAME]

Calculate new video start timestamp from track start time, track event delta and video event delta

options:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -tt TRACK_EVENT_TIME, --track-event-time TRACK_EVENT_TIME
                        Track absolute event time in ISO 8601 format (ex: "2010-10-01 10:00:00")
  -td TRACK_EVENT_DELTA, --track-event-delta TRACK_EVENT_DELTA
                        Track event time in minutes and seconds from track start (ex: "0:10")
  -vd VIDEO_EVENT_DELTA, --video-event-delta VIDEO_EVENT_DELTA
                        Video event time in minutes and seconds from video start (ex: "0:20")
  -vf VIDEO_FILE_NAME, --video-file_name VIDEO_FILE_NAME
                        optional video file name to which we will add metadata
```

# Example Usage

#### To get the correct timestamp for a video file:
1. Identify an event that you can see happen in the track file and in the video (i.e. start taxi)
2. Determine the absolute time of the event in the track file (i.e. 2020-01-10 10:00:00).
3. Then determine the offset time of the event in the track file (i.e. 0:10 into the video).
4. Then determine the offset time of the same event in the video file(i.e. 0:20 into the video).
5. Then run the following command to calculate the new video start timestamp:
    ```
    $ tvts -tt "2020-01-10 10:00:00" -td "0:10" -vd "0:20"
    new video start timestamp: 20200110T095950Z
    ```
6. Add the new video start timestamp to the video file name (i.e. `sockeye-dcs-20200110T095950Z.mp4`)

#### To add the timestamp as metadata to a file, add the -vf argument:
```
$ tvts -tt "2020-01-10 10:00:00" -td "0:10" -vd "0:20" -vf sockeye-dcs.mp4
new video start timestamp: 20200110T095950Z
INFO:root:Adding metadata to file sockeye-dcs.mp4 - ['Media Created': '20200110T095950Z']
```

------
# Developer Setup

## Requirements
- python3.6+
- poetry

## Setup
```
git clone https://github.com/peterb154/tacview-timesync.git
cd tacview-timesync
poetry install
make test
```
