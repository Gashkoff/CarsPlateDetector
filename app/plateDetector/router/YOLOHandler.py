from fastapi import APIRouter
from fastapi import Depends, HTTPException
from common.logger import logger
from detector.PlateDetector import DetectPlates
from detector.SymbolsDetector import SymbolsDetector
from configs.schemas import *
from typing import Annotated
from common.error import YOLOError

router = APIRouter(
    prefix="/api",
    tags=["YOLO detection service"],
)

plateDetector = DetectPlates()
symbolsDetector = SymbolsDetector()

def get_video(request_body: RequestVideo) -> RequestVideo:
    """Can add any """
    return request_body

@router.post("")
def get_detections(
        video: Annotated[RequestVideo, Depends(get_video)],
) -> DetectorResponse:
    """
    Method for Video processing from the user

    The received video from the user is first recognized through the number detection model,
    and then through the number character detection model. Both models are pre-trained yolo11n.pt

    Args:
        video (Annotated[RequestVideo, Depends()]): Video name, stored in a shared directory for docker containers

    Raises:
        YOLOError: If we receive an error from the model during video processing
        Exception: If we receive an error from the backend(hidden for users)
    """
    logger.info(f"Received a message from a user with a video '{video.video_name}'", extra={"servicename": "YOLOHandler"})

    try:
        plateDetector.detect_plate(video.video_name)

    except YOLOError as _yex:
        raise HTTPException(status_code=409, detail=str(_yex))

    except Exception as _ex:
        logger.error(f"An error occurred: {_ex}", extra={"servicename": "YOLOHandler"})
        raise HTTPException(status_code=500, detail=f"Something went wrong")

    try:
        plates, msg = symbolsDetector.detect_symbols()

    except Exception as _ex:
        logger.error(f"An error occurred: {_ex}", extra={"servicename": "YOLOHandler"})
        raise HTTPException(status_code=500, detail=f"Something went wrong")

    return DetectorResponse(symbols=plates, error_message=msg)
