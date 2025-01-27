import os
import cv2
from common.logger import logger
from common.error import YOLOError
from ultralytics import YOLO
from configs.config import *


class DetectPlates:
    """
    class to detect plates from a video.

    This class is initialized with the trained yolo11n model, with the 'mp4v' video codec installed,
    and creates a directory to save the detected license plates. Uses Object Tracking in the process.
    """
    def __init__(self):
        self.model = YOLO(MODEL_PLATE_PATH)
        self.model.overrides['verbose'] = False
        self.fourcc = cv2.VideoWriter.fourcc(*'mp4v')
        os.makedirs(PHOTO_PATH, exist_ok=True)

    @staticmethod
    def delete_photos():
        """Deletes past photos of rooms to add new ones."""
        try:
            for filename in os.listdir(PHOTO_PATH):
                file_path = os.path.join(PHOTO_PATH, filename)
                os.remove(file_path)

            logger.info("Cleared photos directory", extra={'servicename': 'PlateDetector'})

        except OSError as _ex:
            logger.error(f"Error with clear photos directory: {_ex}", extra={'servicename': 'PlateDetector'})
            return _ex

    def detect_plate(self, video: str):
        """Method for detecting plates from a video."""
        logger.info(f"Starting processing video - {video}...", extra={'servicename': 'PlateDetector'})
        err = self.delete_photos()
        if err:
            raise OSError(err)

        cap = cv2.VideoCapture(f'{VIDEO_PATH}/{video}')
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter(f'{VIDEO_PATH}/processing_video.MOV', self.fourcc, fps, (width, height))
        detected_ids = set()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            results = self.model.track(frame, persist=True)

            for item in results:
                boxes = item.boxes

                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = box.conf[0]
                    cls = int(box.cls[0])
                    detection_id = int(box.id[0]) if box.id else None
                    label = f'{self.model.names[cls]} {conf:.2f}'

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    if detection_id is not None and detection_id not in detected_ids and conf >= 0.75:
                        detected_ids.add(detection_id)
                        plate = frame[y1:y2, x1:x2]
                        filename = f'{PHOTO_PATH}/plate_{detection_id}.png'
                        cv2.imwrite(filename, plate)

            out.write(frame)

        self.model = YOLO(MODEL_PLATE_PATH)

        logger.info(f'Video processing is finished', extra={'servicename': 'PlateDetector'})
        cap.release()
        out.release()

        if not os.listdir(PHOTO_PATH):
            raise YOLOError("Couldn't recognize the number in the photo")

# if __name__ == '__main__':
#     yolo = DetectPlates()
#     yolo.detect_plate('IMG_1499.MOV')

