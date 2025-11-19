from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Eros Health Monitor"
    
    REST_PORT: int = 8080
    GRPC_PORT: int = 50051
    SSE_INTERVAL: int = 5
    
    GEO_GRPC_TARGET: str = "charts-eternal-eu-geo-test.charts-eternal-eu-geo-test:50051"
    APP_ENVIRONMENT: str = "test"
    APP_DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False 

settings = Settings()