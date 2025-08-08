import logging
import os
import sys
from typing import Optional

def setup_logger(
    name: str = "mealie_mcp",
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if logger.handlers:
        return logger
    formatter = logging.Formatter(log_format)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger

LOG_LEVEL = os.environ.get("MEALIE_MCP_LOG_LEVEL", "INFO").upper()
LOG_FILE = os.environ.get("MEALIE_MCP_LOG_FILE", None)
LOG_LEVEL_MAP = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}
logger = setup_logger(level=LOG_LEVEL_MAP.get(LOG_LEVEL, logging.INFO), log_file=LOG_FILE)
