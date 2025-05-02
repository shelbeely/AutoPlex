from loguru import logger
import yaml
import os
from functools import partial

# Load configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Get log level from config
LOG_LEVEL = config['app']['log_level']

# Remove default logger
logger.remove()

# Create a custom log format with a quirky trans femme aesthetic 🌈✨
def formatter(record):
    level = record["level"].name
    emoji = {
        "TRACE": "🔍",
        "DEBUG": "🧪",
        "INFO": "✨",
        "SUCCESS": "🎉",
        "WARNING": "⚠️",
        "ERROR": "🔥",
        "CRITICAL": "💀"
    }.get(level, "📝")
    
    return (
        f"<green>{record['time'].strftime('%Y-%m-%d %H:%M:%S')}</green> | "
        f"<level>{level}</level> | "
        f"{emoji} <cyan>{record['name']}</cyan>:<cyan>{record['function']}</cyan>:<cyan>{record['line']}</cyan> - "
        f"<level>{record['message']}</level>\n"
    )

# Add console logger
logger.add(
    lambda msg: print(msg, end=''),
    format=formatter,
    level=LOG_LEVEL,
    colorize=True
)

# Add file logger for structured logging
logger.add(
    "logs/autoplex_{time}.log",
    format="{time} | {level} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    rotation="10 MB",
    retention="7 days",
    compression="zip"
)

# Create a partial function for getting module-specific loggers
get_logger = partial(logger.bind, component="AutoPlex")

# Example usage:
# from src.utils.logging import get_logger
# log = get_logger(__name__)
# log.info("Starting up AutoPlex 🚀")
