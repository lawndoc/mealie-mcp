import logging
import os
import sys
from typing import Optional


def setup_logger(
    name: str = "mealie-mcp",
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
) -> logging.Logger:
    """
    Configure and return a logger instance.
    
    Args:
        name: The name of the logger
        level: The logging level (default: INFO)
        log_file: Optional path to a log file
        log_format: The format string for log messages
        
    Returns:
        A configured logger instance
    """
    # Get or create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(log_format)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# Environment variable to control log level
LOG_LEVEL = os.environ.get("MEALIE_MCP_LOG_LEVEL", "INFO").upper()
LOG_FILE = os.environ.get("MEALIE_MCP_LOG_FILE", None)

# Map string log levels to their numeric values
LOG_LEVEL_MAP = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

# Configure the root logger
logger = setup_logger(
    level=LOG_LEVEL_MAP.get(LOG_LEVEL, logging.INFO),
    log_file=LOG_FILE,
)