import logging
import sys
from pathlib import Path
from datetime import datetime

# Create logs directory if it doesn't exist
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Create a timestamp for the log file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = LOGS_DIR / f"tools_{timestamp}.log"


def setup_logger(name: str) -> logging.Logger:
    """
    Setup and return a logger with both file and console handlers.
    
    Args:
        name: Name of the logger (typically the tool name)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Only add handlers if they haven't been added yet
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # File handler - logs everything
        file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        
        # Console handler - logs INFO and above
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger


def log_tool_call(logger: logging.Logger, tool_name: str, **kwargs):
    """
    Log when a tool is called with its parameters.
    
    Args:
        logger: Logger instance
        tool_name: Name of the tool being called
        **kwargs: Parameters passed to the tool
    """
    logger.info(f"{'='*60}")
    logger.info(f"Tool Called: {tool_name}")
    logger.info(f"Parameters:")
    for key, value in kwargs.items():
        # Truncate long values for readability
        str_value = str(value)
        if len(str_value) > 200:
            str_value = str_value[:200] + "... (truncated)"
        logger.info(f"  - {key}: {str_value}")
    logger.info(f"{'='*60}")


def log_tool_output(logger: logging.Logger, tool_name: str, output: str, success: bool = True):
    """
    Log the output of a tool execution.
    
    Args:
        logger: Logger instance
        tool_name: Name of the tool
        output: Output from the tool
        success: Whether the tool executed successfully
    """
    logger.info(f"{'-'*60}")
    logger.info(f"Tool Output: {tool_name}")
    logger.info(f"Status: {'SUCCESS' if success else 'FAILED'}")
    
    # Truncate very long outputs for console, but log full output to file
    if len(output) > 1000:
        logger.info(f"Output (truncated): {output[:1000]}...")
        logger.debug(f"Full Output: {output}")
    else:
        logger.info(f"Output: {output}")
    
    logger.info(f"{'-'*60}\n")


def log_tool_error(logger: logging.Logger, tool_name: str, error: Exception):
    """
    Log errors that occur during tool execution.
    
    Args:
        logger: Logger instance
        tool_name: Name of the tool
        error: Exception that was raised
    """
    logger.error(f"{'!'*60}")
    logger.error(f"Tool Error: {tool_name}")
    logger.error(f"Error Type: {type(error).__name__}")
    logger.error(f"Error Message: {str(error)}")
    logger.error(f"{'!'*60}\n")
    logger.exception("Full traceback:")
