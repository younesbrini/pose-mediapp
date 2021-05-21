from orion.utils import DATA_PATH, WEB_PATH
import uvicorn, asyncio, cv2
from vidgear.gears.asyncio import WebGear_RTC
from av import VideoFrame
from aiortc import VideoStreamTrack
from vidgear.gears.asyncio import WebGear_RTC
from vidgear.gears.asyncio.helper import reducer
# # import required libraries
# import os

# # enforce UDP
# os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

# various performance tweaks
options = {
    "frame_size_reduction": 30,
    "overwrite_default_files": False,
    "enable_live_broadcast": True,
    "custom_data_location": str(WEB_PATH / "assets"),
}

# initialize WebGear_RTC app
web = WebGear_RTC(logging=True, **options)

# create your own Bare-Minimum Custom Media Server
class Custom_RTCServer(VideoStreamTrack):
    """
    Custom Media Server using OpenCV, an inherit-class
    to aiortc's VideoStreamTrack.
    """

    def __init__(self, source=None):

        # don't forget this line!
        super().__init__()

        # initialize global params
        self.stream = cv2.VideoCapture(source)

    async def recv(self):
        """
        A coroutine function that yields `av.frame.Frame`.
        """
        # don't forget this function!!!

        # get next timestamp
        pts, time_base = await self.next_timestamp()

        # read video frame
        (grabbed, frame) = self.stream.read()

        # if NoneType
        if not grabbed:
            return None

        # reducer frames size if you want more performance otherwise comment this line
        frame = await reducer(frame, percentage=30)  # reduce frame by 30%

        # contruct `av.frame.Frame` from `numpy.nd.array`
        av_frame = VideoFrame.from_ndarray(frame, format="bgr24")
        av_frame.pts = pts
        av_frame.time_base = time_base

        # return `av.frame.Frame`
        return av_frame

    def terminate(self):
        """
        Gracefully terminates VideoGear stream
        """
        # don't forget this function!!!

        # terminate
        if not (self.stream is None):
            self.stream.release()
            self.stream = None


# assign your custom media server to config with adequate source (for e.g. foo.mp4)
web.config["server"] = Custom_RTCServer(source=str(DATA_PATH / "videos" / "foo.mp4"))

uvicorn.run(web(), host="0.0.0.0", port=8080)

# close app safely
web.shutdown()