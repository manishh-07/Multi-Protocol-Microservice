import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.rest.router import router as health_router
from app.api.grpc.server import start_grpc_server
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initialization: Starting gRPC server...")
    grpc_server = await start_grpc_server()
    
    yield  
    
    print("Shutdown signal received. Stopping gRPC server gracefully...")
    await grpc_server.stop(grace=5)
    print("gRPC Server stopped. Bye!")

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

app.include_router(health_router, prefix="/api/health-poc")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=settings.REST_PORT, 
        reload=False
    )