import time
from fastapi import Request, HTTPException

# Simple in-memory rate limiter (per IP)
RATE_LIMIT = 3  # max requests
RATE_PERIOD = 60  # seconds
_requests = {}

def check_rate_limit(request: Request):
    ip = request.client.host
    now = time.time()
    reqs = _requests.get(ip, [])
    # Remove expired requests
    reqs = [t for t in reqs if now - t < RATE_PERIOD]
    if len(reqs) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too many requests. Please wait before retrying.")
    reqs.append(now)
    _requests[ip] = reqs
