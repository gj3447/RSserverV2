from fastapi import APIRouter, Depends, Response
from typing import Annotated
import cv2
import numpy as np

from service.camera_service import CameraService
from dependencies import get_camera_service

router = APIRouter(prefix="/camera", tags=["camera"])

@router.get("/frames")
async def get_frames(
    camera_service: Annotated[CameraService, Depends(get_camera_service)]
):
    frames = camera_service.get_frames()
    
    if not frames["color"] or not frames["depth"]:
        return {"error": "No frames available"}
    
    depth_colormap = cv2.applyColorMap(
        cv2.convertScaleAbs(frames["depth"], alpha=0.03),
        cv2.COLORMAP_JET
    )
    
    combined_frame = np.hstack((frames["color"], depth_colormap))
    
    _, buffer = cv2.imencode('.jpg', combined_frame)
    
    return Response(
        content=buffer.tobytes(),
        media_type="image/jpeg"
    )

@router.get("/imu")
async def get_imu_data(
    camera_service: Annotated[CameraService, Depends(get_camera_service)]
):
    frames = camera_service.get_frames()
    return {
        "accelerometer": frames["accel"],
        "gyroscope": frames["gyro"]
    }