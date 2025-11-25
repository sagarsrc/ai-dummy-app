"""Rate limiting middleware."""

import time
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

# Simple in-memory rate limiter (use Redis in production)
request_counts = {}
RATE_LIMIT = 100  # requests per minute
WINDOW = 60  # seconds


class RateLimiterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        # Clean old entries
        request_counts[client_ip] = [
            t for t in request_counts.get(client_ip, [])
            if current_time - t < WINDOW
        ]

        # Check rate limit
        if len(request_counts.get(client_ip, [])) >= RATE_LIMIT:
            retry_after = WINDOW - (current_time - request_counts[client_ip][0])
            return JSONResponse(
                status_code=429,
                content={
                    "error": "rate_limit_exceeded",
                    "message": "Too many requests",
                    "retry_after": int(retry_after),
                },
                headers={"Retry-After": str(int(retry_after))},
            )

        # Record request
        if client_ip not in request_counts:
            request_counts[client_ip] = []
        request_counts[client_ip].append(current_time)

        return await call_next(request)
