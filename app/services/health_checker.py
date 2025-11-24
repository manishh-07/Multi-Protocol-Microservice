import grpc
from app.generated import health_pb2, health_pb2_grpc
from app.core.config import settings

class HealthChecker:
    @staticmethod
    async def perform_check() -> dict:
        """
        Connects to Geo Service via gRPC to check its status.
        """
        target = settings.GEO_GRPC_TARGET
        
        try:
            # Create a gRPC channel to Geo Service
            # timeout=2 ensures we don't wait forever if Geo is down
            async with grpc.aio.insecure_channel(target) as channel:
                stub = health_pb2_grpc.HealthServiceStub(channel)
                
                response = await stub.Check(
                    health_pb2.HealthRequest(service_name="Health-Monitor-App"),
                    timeout=2
                )
                
                return {"monitor_target": "EU-Geo Service","status": response.status,"is_healthy": response.is_healthy,"remote_component": response.component,"connection": "gRPC Connected "}
                
        except grpc.RpcError as e:
            return {"monitor_target": "EU-Geo Service","status": "Down","is_healthy": False,"error": str(e.code()),"details": e.details(),"connection": "Failed "}
        except Exception as e:
            return {"monitor_target": "EU-Geo Service","status": "Error","is_healthy": False,"error": str(e),"connection": "Failed "}