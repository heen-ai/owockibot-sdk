"""Custom exceptions for the owockibot SDK."""

from typing import Optional, Dict, Any


class OwockibotError(Exception):
    """Base exception for all owockibot SDK errors."""
    
    def __init__(self, message: str, response: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.message = message
        self.response = response


class APIError(OwockibotError):
    """Raised when the API returns an error response."""
    
    def __init__(
        self,
        message: str,
        status_code: int,
        response: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message, response)
        self.status_code = status_code


class NotFoundError(APIError):
    """Raised when a requested resource is not found (404)."""
    
    def __init__(
        self,
        message: str = "Resource not found",
        response: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message, 404, response)


class ValidationError(APIError):
    """Raised when request validation fails (400)."""
    
    def __init__(
        self,
        message: str = "Validation failed",
        response: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message, 400, response)


class RateLimitError(APIError):
    """Raised when rate limit is exceeded (429)."""
    
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[int] = None,
        response: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message, 429, response)
        self.retry_after = retry_after


class ServerError(APIError):
    """Raised when server encounters an error (5xx)."""
    
    def __init__(
        self,
        message: str = "Server error",
        status_code: int = 500,
        response: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message, status_code, response)


class AuthenticationError(APIError):
    """Raised when authentication fails (401)."""
    
    def __init__(
        self,
        message: str = "Authentication failed",
        response: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message, 401, response)


class PaymentError(OwockibotError):
    """Raised when payment/x402 processing fails."""
    
    def __init__(
        self,
        message: str,
        payment_details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message)
        self.payment_details = payment_details
