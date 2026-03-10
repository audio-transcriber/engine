import signal
from contextlib import contextmanager
from typing import Generator

import whisper

import application.containers
from config.minio import minio_settings
from config.rabbitmq import rabbitmq_settings
from config.loguru import worker_logger
import infrastructure.containers
from infrastructure.rabbitmq import transcription_todo_callback

model = whisper.load_model('base')

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


class BreakException(Exception):
    pass


def handler(signum, frame):
    raise BreakException


signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)


@contextmanager
def lifespan() -> Generator[None, None, None]:
    rabbitmq_container.init_resources()
    worker_logger.debug('Ресурсы инициализированы')
    yield
    rabbitmq_container.shutdown_resources()
    worker_logger.debug('Ресурсы остановлены')


def main() -> None:
    with lifespan():
        while True:
            worker_logger.info('Приложение запущено')
            try:
                rabbitmq_container.consumer().consume(
                    'transcription_todo', transcription_todo_callback(transcription_container.usecase())
                )
            except BreakException:
                worker_logger.info('Приложение остановлено')
                break
            except Exception as e:
                worker_logger.exception(e)


if __name__ == '__main__':
    main()
