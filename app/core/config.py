from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Eros Health Monitor"
    REST_PORT: int = 8080
    GRPC_PORT: int = 50051
    SSE_INTERVAL: int = 5
    
    # NEW: Geo Service Address
    # Format: <service-name>.<namespace>:50051
    # Adjust namespace if Geo is in a different one
    GEO_GRPC_TARGET: str = "charts-eternal-eu-geo.charts-eternal-eu-geo:50051"
    
    class Config:
        env_file = ".env"

settings = Settings()