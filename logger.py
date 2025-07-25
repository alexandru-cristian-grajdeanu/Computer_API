import logging
import os

logger = logging.getLogger("math_microservice")
logger.setLevel(logging.INFO)

if not logger.hasHandlers():
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    file_handler = logging.FileHandler(
        f"{log_dir}/app.log", mode="a", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
