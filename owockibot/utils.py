"""Utility functions for the owockibot SDK."""

from decimal import Decimal
from typing import List, Dict, Any

from .models import Bounty


def usdc_to_micro(usdc: Decimal) -> int:
    """Convert USDC amount to micro-USDC (6 decimal places).
    
    Args:
        usdc: USDC amount as Decimal
        
    Returns:
        Amount in micro-USDC (integer)
        
    Example:
        >>> usdc_to_micro(Decimal("10.50"))
        10500000
    """
    return int(usdc * Decimal(1_000_000))


def micro_to_usdc(micro: int) -> Decimal:
    """Convert micro-USDC to USDC amount.
    
    Args:
        micro: Amount in micro-USDC
        
    Returns:
        USDC amount as Decimal
        
    Example:
        >>> micro_to_usdc(10500000)
        Decimal('10.5')
    """
    return Decimal(micro) / Decimal(1_000_000)


def format_usdc(amount: Decimal) -> str:
    """Format USDC amount with proper decimals.
    
    Args:
        amount: USDC amount
        
    Returns:
        Formatted string (e.g., "10.50 USDC")
    """
    return f"{amount:.2f} USDC"


def calculate_total_value(bounties: List[Bounty]) -> Decimal:
    """Calculate total value of a list of bounties.
    
    Args:
        bounties: List of Bounty objects
        
    Returns:
        Total USDC value
    """
    return sum((b.reward_usdc for b in bounties), Decimal(0))


def calculate_average_reward(bounties: List[Bounty]) -> Decimal:
    """Calculate average reward of a list of bounties.
    
    Args:
        bounties: List of Bounty objects
        
    Returns:
        Average USDC reward
    """
    if not bounties:
        return Decimal(0)
    return calculate_total_value(bounties) / len(bounties)


def get_unique_tags(bounties: List[Bounty]) -> List[str]:
    """Get all unique tags from a list of bounties.
    
    Args:
        bounties: List of Bounty objects
        
    Returns:
        Sorted list of unique tags
    """
    tags: set = set()
    for bounty in bounties:
        tags.update(bounty.tags)
    return sorted(tags)


def group_by_status(bounties: List[Bounty]) -> Dict[str, List[Bounty]]:
    """Group bounties by their status.
    
    Args:
        bounties: List of Bounty objects
        
    Returns:
        Dictionary mapping status to list of bounties
    """
    result: Dict[str, List[Bounty]] = {}
    for bounty in bounties:
        status = bounty.status.value
        if status not in result:
            result[status] = []
        result[status].append(bounty)
    return result


def group_by_tag(bounties: List[Bounty]) -> Dict[str, List[Bounty]]:
    """Group bounties by tags (bounties may appear in multiple groups).
    
    Args:
        bounties: List of Bounty objects
        
    Returns:
        Dictionary mapping tag to list of bounties
    """
    result: Dict[str, List[Bounty]] = {}
    for bounty in bounties:
        for tag in bounty.tags:
            tag_lower = tag.lower()
            if tag_lower not in result:
                result[tag_lower] = []
            result[tag_lower].append(bounty)
    return result


def truncate_address(address: str, chars: int = 4) -> str:
    """Truncate Ethereum address for display.
    
    Args:
        address: Full Ethereum address
        chars: Number of characters to show at start and end
        
    Returns:
        Truncated address (e.g., "0x1234...5678")
    """
    if len(address) <= chars * 2 + 2:
        return address
    return f"{address[:chars + 2]}...{address[-chars:]}"
