import pyrealsense2 as rs
from settings import Settings

class PipelineService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        self.config.enable_stream(
            rs.stream.depth,
            settings.rs_width,
            settings.rs_height,
            rs.format.z16,
            settings.rs_fps
        )

        self.config.enable_stream(
            rs.stream.color,
            settings.rs_width,
            settings.rs_height,
            rs.format.bgr8,
            settings.rs_fps
        )

        self.config.enable_stream(
            rs.stream.accel,
            rs.format.motion_xyz32f,
            200
        )
        self.config.enable_stream(
            rs.stream.gyro,
            rs.format.motion_xyz32f,
            200
        )

        self.align = rs.align(rs.stream.color)
        self._started = False

    def start(self):
        if not self._started:
            self.pipeline.start(self.config)
            self._started = True

    def stop(self):
        if self._started:
            self.pipeline.stop()
            self._started = False

    def get_frames(self):
        frames = self.pipeline.wait_for_frames()
        aligned_frames = self.align.process(frames)

        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()
        accel_frame = frames.first_or_default(rs.stream.accel)
        gyro_frame = frames.first_or_default(rs.stream.gyro)

        return {
            "color": color_frame,
            "depth": depth_frame,
            "accel": accel_frame.as_motion_frame().get_motion_data() if accel_frame else None,
            "gyro": gyro_frame.as_motion_frame().get_motion_data() if gyro_frame else None
        }