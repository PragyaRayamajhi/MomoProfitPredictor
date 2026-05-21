# our_app/core/loggings.py
import logging
from pathlib import Path

# Create logs folder + file
Path("logs").mkdir(exist_ok=True)
log_file = Path("logs/app.log")

# Create logger
logger = logging.getLogger("momo_app")
logger.setLevel(logging.DEBUG)

# Save to file
file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s"))
logger.addHandler(file_handler)

# Show in terminal (clean & beautiful)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(levelname)s → %(message)s"))
logger.addHandler(console_handler)

logger.info("Logger ready! Pragya's Momo Profit Predictor started!")