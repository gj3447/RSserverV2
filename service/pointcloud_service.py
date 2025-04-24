import numpy as np
import pyrealsense2 as rs
from service.pipeline_service import PipelineService

class PointcloudService:
    def __init__(self, pipeline_service: PipelineService):
        self.pipeline_service = pipeline_service
        self.pc = rs.pointcloud()
        
    def get_pointcloud(self):
        frames = self.pipeline_service.get_frames()
        if not frames["depth"] or not frames["color"]:
            return None
            
        points = self.pc.calculate(frames["depth"])
        self.pc.map_to(frames["color"])
        
        vertices = np.asanyarray(points.get_vertices())
        texture = np.asanyarray(points.get_texture_coordinates())
        
        return {
            "vertices": vertices,
            "texture": texture
        }