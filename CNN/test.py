import logging
import os

LOG_FILE_NAME = "MODEL_NAME" + ".out"
LOG = os.path.join("log", LOG_FILE_NAME)
logging.basicConfig(filename=LOG, filemode="w", level=logging.DEBUG)
logging.info("1")
logging.info("2")
