"""
Logging setup for pipeline.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

LOG_DIR = Path(__file__).parent.parent / 'logs'


def setup_logger(level: str = 'info', channel_id: str = 'default') -> logging.Logger:
    """
    Set up logger with file and console handlers.
    
    Args:
        level: Log level (debug, info, warning, error, critical)
        channel_id: Channel ID for separate log files per channel
    """
    logger = logging.getLogger('pipeline')
    logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    logger.handlers = []
    
    # File handler
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(LOG_DIR / f'{channel_id}.log')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger
