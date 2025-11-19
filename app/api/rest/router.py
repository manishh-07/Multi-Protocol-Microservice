import asyncio
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse, JSONResponse
from app.services.health_checker import HealthChecker
from app.core.config import settings

router = APIRouter()

@router.get("/health", status_code=200)
async def get_health():
    """
    Self Check: Returns 200 OK to tell K8s 'I am alive'.
    Does NOT call Geo Service.
    """
    return {"status": "operational", "service": "Health-Monitor"}


@router.get("/events")
async def sse_stream(request: Request):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                break
            
            # Call Geo Service via gRPC
            # IMPORTANT: Added 'await' because perform_check is async
            data = await HealthChecker.perform_check()
            
            yield f"data: {data}\n\n"
            await asyncio.sleep(settings.SSE_INTERVAL)

    return StreamingResponse(event_generator(), media_type="text/event-stream")