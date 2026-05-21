from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "streamlit_app"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    AUTH_COOKIE_KEY: SecretStr = SecretStr("replace_with_32_byte_hex")
    AGENT_CLI_URL: str = ""
    APP_ENV: str = "local"

    GCS_BUCKET_NAME: str = ""
    GCP_PROJECT_ID: str = ""
    GCP_REGION: str = "us-central1"
    CLOUD_SQL_CONNECTION_NAME: str = ""

    # Docker Compose / Cloud Run inject pre-assembled URLs; local dev assembles them below
    DATABASE_URL: str = ""
    ASYNC_DATABASE_URL: str = ""

    def model_post_init(self, __context: object) -> None:
        base = (
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
        if not self.DATABASE_URL:
            object.__setattr__(self, "DATABASE_URL", f"postgresql+psycopg2://{base}")
        if not self.ASYNC_DATABASE_URL:
            object.__setattr__(self, "ASYNC_DATABASE_URL", f"postgresql+asyncpg://{base}")


settings = Settings()
