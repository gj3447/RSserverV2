from service.pipeline_service import PipelineService

class CameraService:
    def __init__(self, pipeline_service: PipelineService):
        self.pipeline_service = pipeline_service
        self._started = False
    
    def start(self):
        if not self._started:
            self.pipeline_service.start()
            self._started = True
    
    def stop(self):
        if self._started:
            self.pipeline_service.stop()
            self._started = False
    
    def get_frames(self):
        return self.pipeline_service.get_frames()