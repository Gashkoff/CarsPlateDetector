from pydantic import BaseModel

class RequestVideo(BaseModel):
    video_name: str

class DetectorResponse(BaseModel):
    symbols: str
    error_message: str | None
