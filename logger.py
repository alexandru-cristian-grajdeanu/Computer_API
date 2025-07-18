import logging
import os

# Create a logger instance
logger = logging.getLogger("math_microservice")
logger.setLevel(logging.INFO)

# Ensure we don't add handlers multiple times (e.g., in reload)
if not logger.hasHandlers():
    # Create formatter
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    file_handler = logging.FileHandler(f"{log_dir}/app.log", mode="a", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
