import grpc
from app.generated import health_pb2, health_pb2_grpc
from app.services.health_checker import HealthChecker
from app.core.config import settings

class HealthGrpcServicer(health_pb2_grpc.HealthServiceServicer):
    async def Check(self, request, context):
        # Reusing the same logic from Service Layer
        data = HealthChecker.perform_check()
        
        return health_pb2.HealthResponse(
            status=data["status"],
            is_healthy=data["is_healthy"]
        )

async def start_grpc_server():
    server = grpc.aio.server()
    health_pb2_grpc.add_HealthServiceServicer_to_server(HealthGrpcServicer(), server)
    listen_addr = f"[::]:{settings.GRPC_PORT}"
    server.add_insecure_port(listen_addr)
    
    print(f"gRPC Server starting on port {settings.GRPC_PORT}...")
    await server.start()
    return server