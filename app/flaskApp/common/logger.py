import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                              datefmt="%m/%d/%Y %I:%M:%S%p")
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.propagate = False
