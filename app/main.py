import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.rest.router import router as health_router
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Monitor App Starting...")
    yield  
    print("Monitor App Stopping...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

# For now dummy just to ignore cors on frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

app.include_router(health_router, prefix="/api/health-poc")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.REST_PORT, reload=False)