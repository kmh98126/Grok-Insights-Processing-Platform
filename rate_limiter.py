"""Rate limiting for API endpoints."""
from collections import deque
from datetime import datetime, timedelta
from typing import Deque
import asyncio

class RateLimiter:
    """Simple token bucket rate limiter."""
    
    def __init__(self, max_requests: int, time_window: float = 1.0):
        """
        Args:
            max_requests: Maximum number of requests allowed
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: Deque[float] = deque()
        self.lock = asyncio.Lock()
    
    async def acquire(self) -> bool:
        """
        Try to acquire a token. Returns True if allowed, False if rate limited.
        """
        async with self.lock:
            now = datetime.now().timestamp()
            
            # Remove old requests outside the time window
            while self.requests and now - self.requests[0] > self.time_window:
                self.requests.popleft()
            
            # Check if we're at the limit
            if len(self.requests) >= self.max_requests:
                return False
            
            # Add current request
            self.requests.append(now)
            return True
    
    async def get_retry_after(self) -> int:
        """Get seconds to wait before retry."""
        async with self.lock:
            if not self.requests:
                return 0
            
            oldest_request = self.requests[0]
            now = datetime.now().timestamp()
            elapsed = now - oldest_request
            retry_after = max(0, int(self.time_window - elapsed) + 1)
            return retry_after


# Global rate limiters
# Inbound: 100 requests/second
inbound_limiter = RateLimiter(max_requests=100, time_window=1.0)

