from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "AI-Powered Web Security Assessment Platform"
    app_version: str = "0.1.0"
    debug: bool = False
    database_url: str = "sqlite:///./security_assessment.db"
    report_dir: str = "../reports"
    request_timeout_seconds: float = 8.0
    cors_origins: list[str] = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "https://web-security-assessment-platform.vercel.app"
]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="SAP_",
    )


settings = Settings()
