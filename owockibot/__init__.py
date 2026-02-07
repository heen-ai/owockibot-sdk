"""
owockibot - Python SDK for the AI Bounty Board API

A clean, type-hinted Python client for interacting with the owockibot
bounty board at https://bounty.owockibot.xyz

Example:
    >>> from owockibot import BountyBoardClient
    >>> client = BountyBoardClient()
    >>> bounties = client.list_bounties()
    >>> print(f"Found {len(bounties)} bounties")
"""

from .client import BountyBoardClient
from .models import (
    Bounty,
    Stats,
    Submission,
    Rejection,
    PendingPayment,
    Payment,
    X402Config,
    TokenConfig,
    BountyStatus,
)
from .exceptions import (
    OwockibotError,
    APIError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError,
)
from .filters import BountyFilter

__version__ = "0.1.0"
__all__ = [
    "BountyBoardClient",
    "Bounty",
    "Stats",
    "Submission",
    "Rejection",
    "PendingPayment",
    "Payment",
    "X402Config",
    "TokenConfig",
    "BountyStatus",
    "OwockibotError",
    "APIError",
    "NotFoundError",
    "ValidationError",
    "RateLimitError",
    "ServerError",
    "BountyFilter",
]
