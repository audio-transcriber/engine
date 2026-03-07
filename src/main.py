from contextlib import contextmanager, suppress
from typing import Generator

import whisper

import application.containers
import config
import infrastructure.containers
from infrastructure.rabbitmq import transcription_todo_callback

model = whisper.load_model('base')

minio_settings = config.MinIOSettings()
rabbitmq_settings = config.RabbitMQSettings()

whisper_container = infrastructure.containers.WhisperContainer(model=model)
minio_container = infrastructure.containers.MinIOContainer(
    endpoint_url=minio_settings.endpoint_url,
    secret_key=minio_settings.secret_key,
    access_key=minio_settings.access_key,
)
rabbitmq_container = infrastructure.containers.RabbitMQContainer(
    host=rabbitmq_settings.host,
    port=rabbitmq_settings.port,
)
transcription_container = application.containers.TranscriptionContainer(
    whisper_container=whisper_container,
    minio_container=minio_container,
    rabbitmq_container=rabbitmq_container,
)


@contextmanager
def lifespan() -> Generator[None, None, None]:
    rabbitmq_container.init_resources()
    try:
        with suppress(KeyboardInterrupt):
            yield
    finally:
        rabbitmq_container.shutdown_resources()


def main() -> None:
    with lifespan():
        rabbitmq_container.consumer().consume(
            'transcription_todo', transcription_todo_callback(transcription_container.usecase())
        )


if __name__ == '__main__':
    main()
