"""
Utility functions for vulnemon
"""

import logging
from typing import Any, Dict


logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO") -> None:
    """
    Configure logging for vulnemon
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def format_result(status: str, message: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Format standard result dictionary
    
    Args:
        status: Result status
        message: Descriptive message
        data: Optional data payload
    
    Returns:
        Formatted result dictionary
    """
    return {
        "status": status,
        "message": message,
        "data": data or {}
    }


def validate_input(value: Any, expected_type: type) -> bool:
    """
    Validate input against expected type
    
    Args:
        value: Value to validate
        expected_type: Expected Python type
    
    Returns:
        True if valid, False otherwise
    """
    try:
        return isinstance(value, expected_type)
    except Exception as e:
        logger.error(f"Validation error: {e}")
        return False
