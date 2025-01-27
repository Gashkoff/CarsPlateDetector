from ultralytics import YOLO
from common.logger import logger
import os
import re
from configs.config import *


class SymbolsDetector:
    """
    A class for recognizing the characters of a number detected by the DetectPlates class.

    It works with photos and uses a pattern of Russian numbers.
    """
    def __init__(self):
        self.model = YOLO(MODEL_SYMBOLS_PATH)
        self.model.overrides['verbose'] = False
        self.regex = r"^[ABEKMHOPCTYX]\d{3}[ABEKMHOPCTYX]{2}\d{2,3}$"

    def detect_symbols(self) -> (str, str):
        """
        Method for detecting symbols from images.

        Returns:
            plates: A string with all recognized numbers.
            errors: A string with error messages if no number has been recognized.
        """
        logger.info('Starting processing photos', extra={'servicename': 'SymbolsDetector'})
        plates = ''

        for photo in os.listdir(PHOTO_PATH):
            result = self.model(f"{PHOTO_PATH}/{photo}")

            for item in result:
                detections = []

                for box in item.boxes:
                    x1, cls = int(box.xyxy[0][0]), int(box.cls[0])
                    detections.append((x1, cls))

                detections.sort(key=lambda x: x[0])
                sorted_classes = [self.model.names[cls] for _, cls in detections]
                plate = ''.join(sorted_classes)
                if re.match(self.regex, plate):
                    plates += plate + ' '

        logger.info(f'Photos processing is finished: {plates}', extra={'servicename': 'SymbolsDetector'})

        return (plates.rstrip(), None) if plates else ('', 'The number symbols are not recognized')

# if __name__ == "__main__":
#     yolo = SymbolsDetector()
#     yolo.detect_symbols()
