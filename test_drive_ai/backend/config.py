class Settings:
    """Application settings"""

    # API Settings
    HOST: str = "localhost"
    PORT: int = 8000
    DEBUG: bool = True

    # Application Settings
    APP_NAME: str = "Experiment Dashboard"
    API_VERSION: str = "1.0.0"

    # CORS Settings
    CORS_ORIGINS: list = ["http://localhost:8501"]  # noqa: RUF012

    # Experiment Settings
    MAX_CONCURRENT_EXPERIMENTS: int = 5
    EXPERIMENT_TIMEOUT_SECONDS: int = 3600  # 1 hour

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()
