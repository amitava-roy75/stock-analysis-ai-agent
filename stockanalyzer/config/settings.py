from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Stock Analyzer AI"
    app_version: str = "1.0.0"

    aws_region: str = "ap-south-1"
    bedrock_model_id: str = "apac.amazon.nova-lite-v1:0"

    news_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()