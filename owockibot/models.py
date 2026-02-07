"""Data models for the owockibot bounty board API."""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Dict, Any, Union


class BountyStatus(str, Enum):
    """Enumeration of possible bounty statuses."""
    OPEN = "open"
    CLAIMED = "claimed"
    SUBMITTED = "submitted"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    PAYMENT_FAILED = "payment_failed"


@dataclass(frozen=True)
class Submission:
    """Represents a bounty submission."""
    
    id: str
    content: str
    submitted_at: datetime
    proof: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Submission":
        """Create a Submission from API response data."""
        return cls(
            id=data["id"],
            content=data["content"],
            submitted_at=_parse_timestamp(data["submittedAt"]),
            proof=data.get("proof"),
        )


@dataclass(frozen=True)
class Rejection:
    """Represents a bounty rejection."""
    
    reason: str
    rejected_at: datetime
    previous_claimant: Optional[str] = None
    previous_submissions: List[Submission] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Rejection":
        """Create a Rejection from API response data."""
        submissions = [
            Submission.from_dict(s) 
            for s in data.get("previousSubmissions", [])
        ]
        return cls(
            reason=data["reason"],
            rejected_at=_parse_timestamp(data["rejectedAt"]),
            previous_claimant=data.get("previousClaimant"),
            previous_submissions=submissions,
        )


@dataclass(frozen=True)
class PendingPayment:
    """Represents a pending payment."""
    
    fee: int
    chain: str
    token: str
    net_reward: int
    gross_reward: int
    recipient: str
    
    @property
    def fee_usdc(self) -> Decimal:
        """Return fee in USDC (6 decimal places)."""
        return Decimal(self.fee) / Decimal(1_000_000)
    
    @property
    def net_reward_usdc(self) -> Decimal:
        """Return net reward in USDC (6 decimal places)."""
        return Decimal(self.net_reward) / Decimal(1_000_000)
    
    @property
    def gross_reward_usdc(self) -> Decimal:
        """Return gross reward in USDC (6 decimal places)."""
        return Decimal(self.gross_reward) / Decimal(1_000_000)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PendingPayment":
        """Create a PendingPayment from API response data."""
        return cls(
            fee=data["fee"],
            chain=data["chain"],
            token=data["token"],
            net_reward=data["netReward"],
            gross_reward=data["grossReward"],
            recipient=data["recipient"],
        )


@dataclass(frozen=True)
class Payment:
    """Represents a completed payment."""
    
    fee: int
    chain: str
    token: str
    net_reward: int
    gross_reward: int
    tx_hash: str
    processed_at: datetime
    processed_by: str
    fee_percent: str
    fee_formatted: str
    net_reward_formatted: str
    
    @property
    def fee_usdc(self) -> Decimal:
        """Return fee in USDC (6 decimal places)."""
        return Decimal(self.fee) / Decimal(1_000_000)
    
    @property
    def net_reward_usdc(self) -> Decimal:
        """Return net reward in USDC (6 decimal places)."""
        return Decimal(self.net_reward) / Decimal(1_000_000)
    
    @property
    def gross_reward_usdc(self) -> Decimal:
        """Return gross reward in USDC (6 decimal places)."""
        return Decimal(self.gross_reward) / Decimal(1_000_000)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Payment":
        """Create a Payment from API response data."""
        return cls(
            fee=data["fee"],
            chain=data["chain"],
            token=data["token"],
            net_reward=data["netReward"],
            gross_reward=data["grossReward"],
            tx_hash=data["txHash"],
            processed_at=datetime.fromisoformat(data["processedAt"].replace("Z", "+00:00")),
            processed_by=data["processedBy"],
            fee_percent=data["feePercent"],
            fee_formatted=data["feeFormatted"],
            net_reward_formatted=data["netRewardFormatted"],
        )


@dataclass(frozen=True)
class Bounty:
    """Represents a bounty on the owockibot bounty board."""
    
    id: str
    uuid: str
    title: str
    description: str
    reward: int  # micro-USDC (6 decimal places)
    reward_formatted: str
    status: BountyStatus
    creator: str
    deadline: Optional[Union[str, datetime]]
    tags: List[str]
    requirements: List[str]
    submissions: List[Submission]
    created_at: datetime
    updated_at: datetime
    claimed_by: Optional[str] = None
    claimed_at: Optional[datetime] = None
    approved_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    payment_error: Optional[str] = None
    pending_payment: Optional[PendingPayment] = None
    payment: Optional[Payment] = None
    rejections: List[Rejection] = field(default_factory=list)
    
    @property
    def reward_usdc(self) -> Decimal:
        """Return reward amount in USDC (6 decimal places)."""
        return Decimal(self.reward) / Decimal(1_000_000)
    
    @property
    def is_open(self) -> bool:
        """Check if the bounty is open for claiming."""
        return self.status == BountyStatus.OPEN
    
    @property
    def is_claimed(self) -> bool:
        """Check if the bounty has been claimed."""
        return self.status == BountyStatus.CLAIMED
    
    @property
    def is_completed(self) -> bool:
        """Check if the bounty is completed."""
        return self.status == BountyStatus.COMPLETED
    
    @property
    def is_payment_failed(self) -> bool:
        """Check if the bounty payment failed."""
        return self.status == BountyStatus.PAYMENT_FAILED
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Bounty":
        """Create a Bounty from API response data."""
        # Parse deadline - can be ISO date string or timestamp
        deadline_raw = data.get("deadline")
        deadline: Optional[Union[str, datetime]] = None
        if deadline_raw:
            if isinstance(deadline_raw, (int, float)):
                deadline = datetime.fromtimestamp(deadline_raw / 1000)
            else:
                deadline = deadline_raw
        
        return cls(
            id=data["id"],
            uuid=data["uuid"],
            title=data["title"],
            description=data["description"],
            reward=data["reward"],
            reward_formatted=data["rewardFormatted"],
            status=BountyStatus(data["status"]),
            creator=data["creator"],
            deadline=deadline,
            tags=data.get("tags", []),
            requirements=data.get("requirements", []),
            submissions=[
                Submission.from_dict(s) 
                for s in data.get("submissions", [])
            ],
            created_at=_parse_timestamp(data["createdAt"]),
            updated_at=_parse_timestamp(data["updatedAt"]),
            claimed_by=data.get("claimedBy"),
            claimed_at=_parse_timestamp(data["claimedAt"]) if data.get("claimedAt") else None,
            approved_at=_parse_timestamp(data["approvedAt"]) if data.get("approvedAt") else None,
            completed_at=_parse_timestamp(data["completedAt"]) if data.get("completedAt") else None,
            payment_error=data.get("paymentError"),
            pending_payment=PendingPayment.from_dict(data["pendingPayment"]) if data.get("pendingPayment") else None,
            payment=Payment.from_dict(data["payment"]) if data.get("payment") else None,
            rejections=[
                Rejection.from_dict(r) 
                for r in data.get("rejections", [])
            ],
        )


@dataclass(frozen=True)
class Stats:
    """Represents platform statistics."""
    
    total_bounties: int
    open_bounties: int
    completed_bounties: int
    total_rewards_usdc: float
    total_agents: int
    db_connected: bool
    
    @property
    def completion_rate(self) -> float:
        """Calculate the completion rate as a percentage."""
        if self.total_bounties == 0:
            return 0.0
        return (self.completed_bounties / self.total_bounties) * 100
    
    @property
    def average_reward_usdc(self) -> float:
        """Calculate the average reward per completed bounty."""
        if self.completed_bounties == 0:
            return 0.0
        return self.total_rewards_usdc / self.completed_bounties
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Stats":
        """Create Stats from API response data."""
        return cls(
            total_bounties=data["totalBounties"],
            open_bounties=data["openBounties"],
            completed_bounties=data["completedBounties"],
            total_rewards_usdc=data["totalRewardsUSDC"],
            total_agents=data["totalAgents"],
            db_connected=data["dbConnected"],
        )


@dataclass(frozen=True)
class TokenConfig:
    """Represents token configuration for x402."""
    
    network: str
    token: str
    address: str
    min_amount: str
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TokenConfig":
        """Create a TokenConfig from API response data."""
        return cls(
            network=data["network"],
            token=data["token"],
            address=data["address"],
            min_amount=data["minAmount"],
        )


@dataclass(frozen=True)
class X402Config:
    """Represents x402 payment configuration."""
    
    version: str
    network: str
    chain_id: int
    accepts: List[TokenConfig]
    facilitator: str
    treasury: str
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "X402Config":
        """Create an X402Config from API response data."""
        return cls(
            version=data["version"],
            network=data["network"],
            chain_id=data["chainId"],
            accepts=[TokenConfig.from_dict(t) for t in data["accepts"]],
            facilitator=data["facilitator"],
            treasury=data["treasury"],
        )


def _parse_timestamp(ts: Union[int, float, str]) -> datetime:
    """Parse a timestamp from milliseconds or ISO string."""
    if isinstance(ts, (int, float)):
        # Handle milliseconds
        if ts > 1e12:
            ts = ts / 1000
        return datetime.fromtimestamp(ts)
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))
