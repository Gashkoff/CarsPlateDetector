class YOLOError(Exception):
    """Exception for YOLO errors

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message: str):
        self.error_message = message

    def __str__(self):
        return f"{self.error_message}"