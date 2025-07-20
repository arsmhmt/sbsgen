from fastapi import Request, HTTPException
from datetime import datetime

async def check_credits(user):
    today = datetime.utcnow().date()
    if user.last_used.date() != today:
        user.credits_used = 0  # reset daily usage

    if user.is_pro:
        return

    if user.credits_used >= user.daily_credits:
        raise HTTPException(status_code=403, detail="No more free credits today")
