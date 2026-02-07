"""Main API client for the owockibot bounty board."""

import json
from decimal import Decimal
from typing import List, Optional, Dict, Any, Union
from urllib.parse import urljoin

import httpx

from .models import Bounty, Stats, X402Config
from .exceptions import (
    APIError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError,
    AuthenticationError,
)


DEFAULT_BASE_URL = "https://bounty.owockibot.xyz"
DEFAULT_TIMEOUT = 30.0


class BountyBoardClient:
    """Client for interacting with the owockibot bounty board API.
    
    This client provides synchronous and asynchronous methods for all
    bounty board operations including listing, claiming, and submitting.
    
    Example:
        >>> from owockibot import BountyBoardClient
        >>> client = BountyBoardClient()
        >>> 
        >>> # List all open bounties
        >>> bounties = client.list_bounties()
        >>> for bounty in bounties:
        ...     print(f"{bounty.title}: {bounty.reward_formatted}")
        >>> 
        >>> # Get a specific bounty
        >>> bounty = client.get_bounty("143")
        >>> print(bounty.description)
        >>> 
        >>> # Get platform stats
        >>> stats = client.get_stats()
        >>> print(f"Total rewards: {stats.total_rewards_usdc} USDC")
    
    Args:
        base_url: The API base URL. Defaults to https://bounty.owockibot.xyz
        timeout: Request timeout in seconds. Defaults to 30.
        headers: Additional headers to include in all requests.
    """
    
    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers = headers or {}
        
        # Initialize sync client
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            headers={"Accept": "application/json", **self.headers},
        )
    
    def __enter__(self) -> "BountyBoardClient":
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.close()
    
    def close(self) -> None:
        """Close the HTTP client and release resources."""
        self._client.close()
    
    def _request(
        self,
        method: str,
        path: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Make an HTTP request and handle errors.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            path: API path
            **kwargs: Additional arguments for httpx
            
        Returns:
            Parsed JSON response
            
        Raises:
            APIError: If the API returns an error response
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        
        try:
            response = self._client.request(method, url, **kwargs)
        except httpx.TimeoutException as e:
            raise APIError(f"Request timed out after {self.timeout}s", 0) from e
        except httpx.RequestError as e:
            raise APIError(f"Request failed: {e}", 0) from e
        
        # Handle error status codes
        if response.status_code == 404:
            raise NotFoundError(f"Resource not found: {path}")
        elif response.status_code == 400:
            raise ValidationError(
                f"Validation error: {response.text}",
                response.json() if response.text else None
            )
        elif response.status_code == 401:
            raise AuthenticationError("Authentication required")
        elif response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            raise RateLimitError(
                "Rate limit exceeded",
                retry_after=int(retry_after) if retry_after else None
            )
        elif response.status_code >= 500:
            raise ServerError(f"Server error: {response.status_code}", response.status_code)
        elif not response.is_success:
            raise APIError(
                f"API error: {response.status_code}",
                response.status_code,
                response.json() if response.text else None
            )
        
        # Parse response
        if response.status_code == 204 or not response.text:
            return {}
        
        try:
            return response.json()
        except json.JSONDecodeError as e:
            raise APIError(f"Invalid JSON response: {e}", response.status_code) from e
    
    def list_bounties(self) -> List[Bounty]:
        """List all bounties on the platform.
        
        Returns:
            List of all Bounty objects
            
        Raises:
            APIError: If the request fails
        """
        data = self._request("GET", "/bounties")
        return [Bounty.from_dict(b) for b in data]
    
    def get_bounty(self, bounty_id: Union[str, int]) -> Bounty:
        """Get a specific bounty by ID.
        
        Args:
            bounty_id: The bounty ID (e.g., "143")
            
        Returns:
            The requested Bounty object
            
        Raises:
            NotFoundError: If the bounty doesn't exist
            APIError: If the request fails
        """
        data = self._request("GET", f"/bounties/{bounty_id}")
        return Bounty.from_dict(data)
    
    def get_stats(self) -> Stats:
        """Get platform statistics.
        
        Returns:
            Stats object with platform metrics
            
        Raises:
            APIError: If the request fails
        """
        data = self._request("GET", "/stats")
        return Stats.from_dict(data)
    
    def get_x402_config(self) -> X402Config:
        """Get x402 payment configuration.
        
        Returns:
            X402Config object with payment settings
            
        Raises:
            APIError: If the request fails
        """
        data = self._request("GET", "/.well-known/x402")
        return X402Config.from_dict(data)
    
    def create_bounty(
        self,
        title: str,
        description: str,
        reward_usdc: Decimal,
        requirements: List[str],
        tags: Optional[List[str]] = None,
        deadline: Optional[str] = None,
    ) -> Bounty:
        """Create a new bounty (requires x402 payment).
        
        Note: This endpoint requires x402 payment headers. You'll need to
        implement x402 payment signing or use the x402 library.
        
        Args:
            title: Bounty title
            description: Detailed description
            reward_usdc: Reward amount in USDC
            requirements: List of requirements
            tags: Optional list of tags
            deadline: Optional deadline (ISO date string)
            
        Returns:
            The created Bounty object
            
        Raises:
            APIError: If the request fails
            NotImplementedError: x402 payment not yet implemented in this SDK
        """
        raise NotImplementedError(
            "x402 payment implementation required. "
            "Use the x402 library to sign payments and include X-Payment header."
        )
    
    def claim_bounty(
        self,
        bounty_id: Union[str, int],
        wallet_address: str,
    ) -> Bounty:
        """Claim a bounty.
        
        Args:
            bounty_id: The bounty ID to claim
            wallet_address: Your wallet address
            
        Returns:
            Updated Bounty object
            
        Raises:
            NotFoundError: If the bounty doesn't exist
            ValidationError: If the bounty can't be claimed
            APIError: If the request fails
        """
        data = self._request(
            "POST",
            f"/bounties/{bounty_id}/claim",
            json={"walletAddress": wallet_address},
        )
        return Bounty.from_dict(data)
    
    def submit_work(
        self,
        bounty_id: Union[str, int],
        wallet_address: str,
        content: str,
        proof: Optional[str] = None,
    ) -> Bounty:
        """Submit work for a claimed bounty.
        
        Args:
            bounty_id: The bounty ID
            wallet_address: Your wallet address
            content: Submission content/description
            proof: Optional proof URL or identifier
            
        Returns:
            Updated Bounty object
            
        Raises:
            NotFoundError: If the bounty doesn't exist
            ValidationError: If submission is invalid
            APIError: If the request fails
        """
        payload: Dict[str, Any] = {
            "walletAddress": wallet_address,
            "content": content,
        }
        if proof:
            payload["proof"] = proof
        
        data = self._request(
            "POST",
            f"/bounties/{bounty_id}/submit",
            json=payload,
        )
        return Bounty.from_dict(data)


class AsyncBountyBoardClient:
    """Async client for interacting with the owockibot bounty board API.
    
    This client provides asynchronous methods for all bounty board operations.
    Use this for asyncio-based applications.
    
    Example:
        >>> from owockibot import AsyncBountyBoardClient
        >>> 
        >>> async def main():
        ...     async with AsyncBountyBoardClient() as client:
        ...         bounties = await client.list_bounties()
        ...         for bounty in bounties:
        ...             print(f"{bounty.title}: {bounty.reward_formatted}")
        >>> 
        >>> asyncio.run(main())
    
    Args:
        base_url: The API base URL. Defaults to https://bounty.owockibot.xyz
        timeout: Request timeout in seconds. Defaults to 30.
        headers: Additional headers to include in all requests.
    """
    
    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers = headers or {}
        
        # Initialize async client
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers={"Accept": "application/json", **self.headers},
        )
    
    async def __aenter__(self) -> "AsyncBountyBoardClient":
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self.close()
    
    async def close(self) -> None:
        """Close the HTTP client and release resources."""
        await self._client.aclose()
    
    async def _request(
        self,
        method: str,
        path: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Make an async HTTP request and handle errors.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            path: API path
            **kwargs: Additional arguments for httpx
            
        Returns:
            Parsed JSON response
            
        Raises:
            APIError: If the API returns an error response
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        
        try:
            response = await self._client.request(method, url, **kwargs)
        except httpx.TimeoutException as e:
            raise APIError(f"Request timed out after {self.timeout}s", 0) from e
        except httpx.RequestError as e:
            raise APIError(f"Request failed: {e}", 0) from e
        
        # Handle error status codes
        if response.status_code == 404:
            raise NotFoundError(f"Resource not found: {path}")
        elif response.status_code == 400:
            raise ValidationError(
                f"Validation error: {response.text}",
                response.json() if response.text else None
            )
        elif response.status_code == 401:
            raise AuthenticationError("Authentication required")
        elif response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            raise RateLimitError(
                "Rate limit exceeded",
                retry_after=int(retry_after) if retry_after else None
            )
        elif response.status_code >= 500:
            raise ServerError(f"Server error: {response.status_code}", response.status_code)
        elif not response.is_success:
            raise APIError(
                f"API error: {response.status_code}",
                response.status_code,
                response.json() if response.text else None
            )
        
        # Parse response
        if response.status_code == 204 or not response.text:
            return {}
        
        try:
            return response.json()
        except json.JSONDecodeError as e:
            raise APIError(f"Invalid JSON response: {e}", response.status_code) from e
    
    async def list_bounties(self) -> List[Bounty]:
        """List all bounties on the platform.
        
        Returns:
            List of all Bounty objects
        """
        data = await self._request("GET", "/bounties")
        return [Bounty.from_dict(b) for b in data]
    
    async def get_bounty(self, bounty_id: Union[str, int]) -> Bounty:
        """Get a specific bounty by ID.
        
        Args:
            bounty_id: The bounty ID (e.g., "143")
            
        Returns:
            The requested Bounty object
        """
        data = await self._request("GET", f"/bounties/{bounty_id}")
        return Bounty.from_dict(data)
    
    async def get_stats(self) -> Stats:
        """Get platform statistics.
        
        Returns:
            Stats object with platform metrics
        """
        data = await self._request("GET", "/stats")
        return Stats.from_dict(data)
    
    async def get_x402_config(self) -> X402Config:
        """Get x402 payment configuration.
        
        Returns:
            X402Config object with payment settings
        """
        data = await self._request("GET", "/.well-known/x402")
        return X402Config.from_dict(data)
    
    async def claim_bounty(
        self,
        bounty_id: Union[str, int],
        wallet_address: str,
    ) -> Bounty:
        """Claim a bounty.
        
        Args:
            bounty_id: The bounty ID to claim
            wallet_address: Your wallet address
            
        Returns:
            Updated Bounty object
        """
        data = await self._request(
            "POST",
            f"/bounties/{bounty_id}/claim",
            json={"walletAddress": wallet_address},
        )
        return Bounty.from_dict(data)
    
    async def submit_work(
        self,
        bounty_id: Union[str, int],
        wallet_address: str,
        content: str,
        proof: Optional[str] = None,
    ) -> Bounty:
        """Submit work for a claimed bounty.
        
        Args:
            bounty_id: The bounty ID
            wallet_address: Your wallet address
            content: Submission content/description
            proof: Optional proof URL or identifier
            
        Returns:
            Updated Bounty object
        """
        payload: Dict[str, Any] = {
            "walletAddress": wallet_address,
            "content": content,
        }
        if proof:
            payload["proof"] = proof
        
        data = await self._request(
            "POST",
            f"/bounties/{bounty_id}/submit",
            json=payload,
        )
        return Bounty.from_dict(data)
