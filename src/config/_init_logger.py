import sys
from loguru import logger

from config.paths import LOG_DIR

logger.remove()
logger.add(
    LOG_DIR / "momo.log",
    format="{time:MM:DD:HH:mm:ss!UTC} | {level: <8} | {module: <13} | {message}",
    rotation="20 MB",
)
logger.add(
    sys.stdout,
    format="{time:MM:DD:HH:mm:ss!UTC} | {level: <8} | {module: <13} | {message}"
)
