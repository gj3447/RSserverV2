from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    rs_host: str = os.getenv("RS_HOST","0.0.0.0")
    rs_port: int = int(os.getenv("RS_PORT","8000"))
    rs_width: int = int(os.getenv("RS_WIDTH","640"))
    rs_height: int = int(os.getenv("RS_HEIGHT","480"))
    rs_fps: int = int(os.getenv("RS_FPS","30"))

def get_settings():
    return Settings()