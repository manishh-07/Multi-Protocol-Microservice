from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Eros Health Microservice"
    REST_PORT: int = 8080
    GRPC_PORT: int = 50051
    SSE_INTERVAL: int = 5  
    
    class Config:
        env_file = ".env"

settings = Settings()