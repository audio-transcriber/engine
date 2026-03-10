from pydantic_settings import BaseSettings, SettingsConfigDict


class RabbitMQSettings(BaseSettings):
    host: str
    port: int

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='rabbitmq_',
        extra='ignore',
    )


rabbitmq_settings = RabbitMQSettings()
