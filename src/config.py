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


class RabbitMQSettings(BaseSettings):
    host: str
    port: int

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='rabbitmq_',
        extra='ignore',
    )
