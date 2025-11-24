from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Eros Health Monitor"
    REST_PORT: int
    GRPC_PORT: int
    SSE_INTERVAL: int
    GEO_GRPC_TARGET: str
    APP_ENVIRONMENT: str
    APP_DEBUG: bool
    
    class Config:
        env_file = ".env"
        case_sensitive = False 

settings = Settings()