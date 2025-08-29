import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger():
    logger = logging.getLogger("trading_bot")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)

    os.makedirs("logs", exist_ok=True)
    file_handler = RotatingFileHandler("logs/trading.log", maxBytes=1_000_000, backupCount=3)
    file_fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    file_handler.setFormatter(file_fmt)
    file_handler.setLevel(logging.INFO)

    console = logging.StreamHandler()
    console_fmt = logging.Formatter("%(levelname)s | %(message)s")
    console.setFormatter(console_fmt)
    console.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(console)
    return logger
