"""Filter and query builder for bounty searches."""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Dict, Any, Callable

from .models import Bounty, BountyStatus


@dataclass
class BountyFilter:
    """Builder for filtering bounties.
    
    Example:
        >>> filter = (
        ...     BountyFilter()
        ...     .with_status(BountyStatus.OPEN)
        ...     .with_tags("coding", "design")
        ...     .with_min_reward(Decimal("10.00"))
        ... )
        >>> open_bounties = filter.apply(bounties)
    """
    
    statuses: List[BountyStatus] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    min_reward: Optional[Decimal] = None
    max_reward: Optional[Decimal] = None
    creator: Optional[str] = None
    claimed_by: Optional[str] = None
    search_query: Optional[str] = None
    custom_filter: Optional[Callable[[Bounty], bool]] = None
    
    def with_status(self, *statuses: BountyStatus) -> "BountyFilter":
        """Filter by one or more statuses.
        
        Args:
            *statuses: One or more BountyStatus values to include
            
        Returns:
            Self for method chaining
        """
        self.statuses.extend(statuses)
        return self
    
    def with_tags(self, *tags: str) -> "BountyFilter":
        """Filter by tags (bounties must have ALL specified tags).
        
        Args:
            *tags: Tags that bounties must have
            
        Returns:
            Self for method chaining
        """
        self.tags.extend(tags)
        return self
    
    def with_any_tags(self, *tags: str) -> "BountyFilter":
        """Filter by tags (bounties must have ANY of the specified tags).
        
        This creates a custom filter. Use with_tags() for ALL matching.
        
        Args:
            *tags: Tags that bounties may have
            
        Returns:
            Self for method chaining
        """
        tag_set = set(t.lower() for t in tags)
        
        def any_tag_filter(bounty: Bounty) -> bool:
            bounty_tags = set(t.lower() for t in bounty.tags)
            return bool(tag_set & bounty_tags)
        
        self.custom_filter = any_tag_filter
        return self
    
    def with_min_reward(self, amount: Decimal) -> "BountyFilter":
        """Filter by minimum reward amount.
        
        Args:
            amount: Minimum USDC reward
            
        Returns:
            Self for method chaining
        """
        self.min_reward = amount
        return self
    
    def with_max_reward(self, amount: Decimal) -> "BountyFilter":
        """Filter by maximum reward amount.
        
        Args:
            amount: Maximum USDC reward
            
        Returns:
            Self for method chaining
        """
        self.max_reward = amount
        return self
    
    def with_reward_range(self, min_amount: Decimal, max_amount: Decimal) -> "BountyFilter":
        """Filter by reward range.
        
        Args:
            min_amount: Minimum USDC reward
            max_amount: Maximum USDC reward
            
        Returns:
            Self for method chaining
        """
        self.min_reward = min_amount
        self.max_reward = max_amount
        return self
    
    def with_creator(self, creator: str) -> "BountyFilter":
        """Filter by creator wallet address.
        
        Args:
            creator: Ethereum address of the creator
            
        Returns:
            Self for method chaining
        """
        self.creator = creator.lower()
        return self
    
    def with_claimed_by(self, claimant: str) -> "BountyFilter":
        """Filter by claimant wallet address.
        
        Args:
            claimant: Ethereum address of the claimant
            
        Returns:
            Self for method chaining
        """
        self.claimed_by = claimant.lower()
        return self
    
    def search(self, query: str) -> "BountyFilter":
        """Search in title and description (case-insensitive).
        
        Args:
            query: Search string
            
        Returns:
            Self for method chaining
        """
        self.search_query = query.lower()
        return self
    
    def apply(self, bounties: List[Bounty]) -> List[Bounty]:
        """Apply all filters to a list of bounties.
        
        Args:
            bounties: List of Bounty objects to filter
            
        Returns:
            Filtered list of bounties
        """
        result = bounties
        
        if self.statuses:
            result = [b for b in result if b.status in self.statuses]
        
        if self.tags:
            result = [
                b for b in result 
                if all(t.lower() in (tag.lower() for tag in b.tags) for t in self.tags)
            ]
        
        if self.min_reward is not None:
            result = [b for b in result if b.reward_usdc >= self.min_reward]
        
        if self.max_reward is not None:
            result = [b for b in result if b.reward_usdc <= self.max_reward]
        
        if self.creator:
            result = [b for b in result if b.creator.lower() == self.creator]
        
        if self.claimed_by:
            result = [
                b for b in result 
                if b.claimed_by and b.claimed_by.lower() == self.claimed_by
            ]
        
        if self.search_query:
            result = [
                b for b in result
                if (self.search_query in b.title.lower() or 
                    self.search_query in b.description.lower())
            ]
        
        if self.custom_filter:
            result = [b for b in result if self.custom_filter(b)]
        
        return result
    
    def to_query_params(self) -> Dict[str, Any]:
        """Convert filter to query parameters for API requests.
        
        Note: The current API doesn't support server-side filtering,
        but this method prepares for future API enhancements.
        
        Returns:
            Dictionary of query parameters
        """
        params: Dict[str, Any] = {}
        
        if self.statuses:
            params["status"] = ",".join(s.value for s in self.statuses)
        
        if self.tags:
            params["tags"] = ",".join(self.tags)
        
        if self.min_reward:
            params["minReward"] = int(self.min_reward * 1_000_000)
        
        if self.max_reward:
            params["maxReward"] = int(self.max_reward * 1_000_000)
        
        if self.creator:
            params["creator"] = self.creator
        
        if self.search_query:
            params["q"] = self.search_query
        
        return params


def filter_by_tags(bounties: List[Bounty], *tags: str) -> List[Bounty]:
    """Filter bounties by tags (must have ALL tags).
    
    Args:
        bounties: List of bounties to filter
        *tags: Tags that must all be present
        
    Returns:
        Filtered list of bounties
    """
    return BountyFilter().with_tags(*tags).apply(bounties)


def filter_open(bounties: List[Bounty]) -> List[Bounty]:
    """Filter to only open bounties.
    
    Args:
        bounties: List of bounties to filter
        
    Returns:
        List of open bounties
    """
    return BountyFilter().with_status(BountyStatus.OPEN).apply(bounties)


def search_bounties(bounties: List[Bounty], query: str) -> List[Bounty]:
    """Search bounties by title and description.
    
    Args:
        bounties: List of bounties to search
        query: Search query string
        
    Returns:
        Matching bounties
    """
    return BountyFilter().search(query).apply(bounties)


def sort_by_reward(bounties: List[Bounty], descending: bool = True) -> List[Bounty]:
    """Sort bounties by reward amount.
    
    Args:
        bounties: List of bounties to sort
        descending: If True, highest rewards first
        
    Returns:
        Sorted list of bounties
    """
    return sorted(bounties, key=lambda b: b.reward, reverse=descending)


def sort_by_created(bounties: List[Bounty], descending: bool = True) -> List[Bounty]:
    """Sort bounties by creation date.
    
    Args:
        bounties: List of bounties to sort
        descending: If True, newest first
        
    Returns:
        Sorted list of bounties
    """
    return sorted(bounties, key=lambda b: b.created_at, reverse=descending)


def sort_by_deadline(bounties: List[Bounty], descending: bool = False) -> List[Bounty]:
    """Sort bounties by deadline.
    
    Args:
        bounties: List of bounties to sort
        descending: If True, furthest deadlines first
        
    Returns:
        Sorted list of bounties
    """
    # Handle None deadlines by putting them at the end
    def deadline_key(b: Bounty):
        if b.deadline is None:
            return datetime.max if descending else datetime.min
        if isinstance(b.deadline, str):
            return datetime.min
        return b.deadline
    
    return sorted(bounties, key=deadline_key, reverse=descending)
