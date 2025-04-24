from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from dependencies import get_camera_service
from routers import camera, pointcloud

@asynccontextmanager
async def lifespan(app: FastAPI):
    camera_service = get_camera_service()
    camera_service.start()
    yield
    camera_service.stop()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(camera.router)
app.include_router(pointcloud.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}