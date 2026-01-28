"""
Utility functions for expense tracker.
"""

from datetime import datetime


def validate_date(date_str: str) -> str:
    """
    Validate date format (YYYY-MM-DD).
    
    Args:
        date_str: Date string to validate
        
    Returns:
        Validated date string
        
    Raises:
        ValueError: If date format is invalid
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        raise ValueError("date must be YYYY-MM-DD")


def validate_amount(amount: float) -> float:
    """
    Validate amount is positive.
    
    Args:
        amount: Amount to validate
        
    Returns:
        Validated amount
        
    Raises:
        ValueError: If amount is not positive
    """
    if amount <= 0:
        raise ValueError("amount must be > 0")
    return amount


def generate_expense_id(date: str, existing_ids: list[str]) -> str:
    """
    Generate unique expense ID in format EXP-YYYYMMDD-NNNN.
    
    Args:
        date: Date string in YYYY-MM-DD format
        existing_ids: List of existing expense IDs
        
    Returns:
        Unique expense ID
    """
    date_part = date.replace("-", "")
    prefix = f"EXP-{date_part}-"
    last_id = existing_ids[-1]
    next_num = int(last_id.split("-")[-1]) + 1
    
    return f"{prefix}{next_num:04d}"
