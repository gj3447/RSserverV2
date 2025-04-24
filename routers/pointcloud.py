from fastapi import APIRouter, Depends
from typing import Annotated
import numpy as np

from service.pointcloud_service import PointcloudService
from dependencies import get_pointcloud_service

router = APIRouter(prefix="/pointcloud", tags=["pointcloud"])

@router.get("/data")
async def get_pointcloud(
    pointcloud_service: Annotated[PointcloudService, Depends(get_pointcloud_service)]
):
    pc_data = pointcloud_service.get_pointcloud()
    if pc_data is None:
        return {"error": "No pointcloud data available"}
    
    return {
        "vertices": pc_data["vertices"].tolist(),
        "texture": pc_data["texture"].tolist()
    }