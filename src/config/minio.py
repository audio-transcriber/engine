from pydantic_settings import BaseSettings, SettingsConfigDict


class MinIOSettings(BaseSettings):
    endpoint_url: str
    access_key: str
    secret_key: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='minio_',
        extra='ignore',
    )


minio_settings = MinIOSettings()
