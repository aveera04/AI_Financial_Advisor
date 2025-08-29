"""
Logger configuration and utilities for Financial Advisor application
"""

import logging
import os
import sys
from datetime import datetime
from typing import Optional
from pathlib import Path


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for different log levels"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }

    def format(self, record):
        # Add color to the levelname
        levelname = record.levelname
        if levelname in self.COLORS:
            colored_levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
            record.levelname = colored_levelname
        
        # Format the message
        formatted = super().format(record)
        
        # Reset the levelname for other formatters
        record.levelname = levelname
        
        return formatted


def get_logger(name: str, level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """
    Create and configure a logger with the given name.
    
    Args:
        name (str): Name of the logger (typically the module name)
        level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file (Optional[str]): Optional file path to write logs to
    
    Returns:
        logging.Logger: Configured logger instance
    """
    
    # Create logger
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Set level
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Create console handler with colored output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Create colored formatter for console
    console_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    console_formatter = ColoredFormatter(console_format, datefmt="%Y-%m-%d %H:%M:%S")
    console_handler.setFormatter(console_formatter)
    
    # Add console handler to logger
    logger.addHandler(console_handler)
    
    # Create file handler if log_file is specified
    if log_file:
        # Create logs directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)  # File gets all levels
        
        # Create plain formatter for file (no colors)
        file_format = "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
        file_formatter = logging.Formatter(file_format, datefmt="%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(file_formatter)
        
        # Add file handler to logger
        logger.addHandler(file_handler)
    
    return logger


def setup_project_logger(log_level: str = "INFO", log_to_file: bool = True) -> None:
    """
    Setup project-wide logging configuration.
    
    Args:
        log_level (str): Default logging level for all loggers
        log_to_file (bool): Whether to write logs to file
    """
    
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Generate log file name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d")
    log_file = logs_dir / f"financial_advisor_{timestamp}.log" if log_to_file else None
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Create and configure handlers
    if log_file:
        get_logger("financial_advisor", log_level, str(log_file))
    else:
        get_logger("financial_advisor", log_level)


# Example usage and testing
if __name__ == "__main__":
    # Test the logger
    test_logger = get_logger("test_logger", "DEBUG")
    
    test_logger.debug("This is a debug message")
    test_logger.info("This is an info message") 
    test_logger.warning("This is a warning message")
    test_logger.error("This is an error message")
    test_logger.critical("This is a critical message")
    
    print("\n--- Testing with file output ---")
    file_logger = get_logger("file_test", "INFO", "logs/test.log")
    file_logger.info("This message will go to both console and file")
    file_logger.error("This error will also be logged to file")
