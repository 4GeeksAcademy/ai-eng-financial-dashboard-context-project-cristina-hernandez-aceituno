"""
Financial data validation and rounding rules.
Implements Financial Data Contract v1.0

This module centralizes all rounding and validation logic for financial values
to ensure consistency across the application. All financial calculations should
use these functions instead of calling round() directly.

Reference: ./.agents/skills/financial-data-contract/SKILL.md
"""

from decimal import Decimal, ROUND_HALF_EVEN
from typing import Optional


def round_currency(value: float | int | Decimal, decimals: int = 2) -> float:
    """
    Round currency using banker's rounding to N decimals.
    
    Args:
        value: The numeric value to round (amount in currency units)
        decimals: Number of decimal places (default: 2 for most currencies)
        
    Returns:
        float: The rounded value
        
    Example:
        >>> round_currency(1234.567)
        1234.57
        >>> round_currency(1234.5)  # Banker's rounding: 4 is even, so round down
        1234.5
        >>> round_currency(1235.5)  # Banker's rounding: 6 is even, so round up
        1235.5
    """
    if value is None:
        return None
    d = Decimal(str(value))
    quantize_exp = Decimal(10) ** -decimals
    return float(d.quantize(quantize_exp, rounding=ROUND_HALF_EVEN))


def round_percent(value: float | int | Decimal, decimals: int = 2) -> Optional[float]:
    """
    Round percentage using banker's rounding to N decimals.
    
    Args:
        value: The numeric value to round (percentage, 0-100)
        decimals: Number of decimal places (default: 2)
        
    Returns:
        float: The rounded value, or None if input is None
        
    Example:
        >>> round_percent(15.235)
        15.24  # With 2 decimals
        >>> round_percent(99.996)
        100.0
    """
    if value is None:
        return None
    d = Decimal(str(value))
    quantize_exp = Decimal(10) ** -decimals
    return float(d.quantize(quantize_exp, rounding=ROUND_HALF_EVEN))


def round_ratio(value: float | int | Decimal, decimals: int = 4) -> Optional[float]:
    """
    Round ratio/index values using banker's rounding to N decimals.
    
    Args:
        value: The numeric value to round (ratio, typically 0-1 or percentage)
        decimals: Number of decimal places (default: 4 for detailed precision)
        
    Returns:
        float: The rounded value, or None if input is None
        
    Example:
        >>> round_ratio(0.12345)
        0.1235  # With 4 decimals
    """
    if value is None:
        return None
    d = Decimal(str(value))
    quantize_exp = Decimal(10) ** -decimals
    return float(d.quantize(quantize_exp, rounding=ROUND_HALF_EVEN))
