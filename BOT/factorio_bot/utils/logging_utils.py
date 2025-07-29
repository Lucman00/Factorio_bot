import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from ..config import Config

def setup_logger(name: str = 'factorio_bot') -> logging.Logger:
    """
    Configure application logging
    :param name: Logger name
    :return: Configured logger instance
    """
    # Ensure logs directory exists
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # File handler (rotates at 5MB)
    file_handler = RotatingFileHandler(
        logs_dir / 'bot.log',
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(levelname)s - %(message)s'
    ))
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Create default logger instance
logger = setup_logger()