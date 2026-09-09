from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    cors_origins: str = "http://localhost:5173"
    max_upload_mb: int = 200
    max_images: int = 2000
    job_ttl_minutes: int = 30
    work_dir: str = "./tmp"

    class Config:
        env_file = ".env"


settings = Settings()