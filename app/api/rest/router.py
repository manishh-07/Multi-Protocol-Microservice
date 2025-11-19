import asyncio
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from app.services.health_checker import HealthChecker
from app.core.config import settings

router = APIRouter()

# REST Endpoint 
@router.get("/health", status_code=200)
async def get_health():
    """
    Standard REST Health Check.
    Returns 200 OK if service is alive.
    """
    result = HealthChecker.perform_check()
    return result

# SSE Endpoint
@router.get("/events")
async def sse_stream(request: Request):
    """
    Server-Sent Events. Emits health status every 5 seconds.
    """
    async def event_generator():
        while True:
            if await request.is_disconnected():
                break
            
            data = HealthChecker.perform_check()
            # SSE format: "data: <payload>\n\n"
            yield f"data: {data}\n\n"
            
            # Requirement: 5 seconds delay
            await asyncio.sleep(settings.SSE_INTERVAL)

    return StreamingResponse(event_generator(), media_type="text/event-stream")