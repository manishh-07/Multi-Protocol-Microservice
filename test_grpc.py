import asyncio
import grpc
from app.generated import health_pb2, health_pb2_grpc

async def test():
    # Connect to localhost:50051
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = health_pb2_grpc.HealthServiceStub(channel)
        print("Connecting to gRPC server...")
        response = await stub.Check(health_pb2.HealthRequest(service_name="test-client"))
        print(f"Response received: Healthy={response.is_healthy}, Status={response.status}")

if __name__ == "__main__":
    asyncio.run(test())