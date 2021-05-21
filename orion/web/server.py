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
web = WebGear_RTC(source=str(DATA_PATH / "videos" / "foo.mp4"), logging=True, **options)

uvicorn.run(web(), host="0.0.0.0", port=8080)

# close app safely
web.shutdown()