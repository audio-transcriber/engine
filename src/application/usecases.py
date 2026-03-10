import json
from io import BytesIO
from pathlib import Path

import loguru

from infrastructure.minio import MinIOStorage
from infrastructure.rabbitmq import RabbitMQProducer
from infrastructure.whisper import WhisperTranscriptor


class TranscriptionUseCase:
    def __init__(
        self,
        transcriptor: WhisperTranscriptor,
        storage: MinIOStorage,
        rabbitmq_producer: RabbitMQProducer,
        logger: loguru.logger,
    ) -> None:
        self._transcriptor = transcriptor
        self._storage = storage
        self._rabbitmq_producer = rabbitmq_producer
        self._logger = logger

    def transcribe(self, filename: str, bucket_name: str) -> None:
        file = BytesIO(self._storage.get(filename, bucket_name))
        new_filename = Path(filename).with_suffix('.txt').name
        self._storage.save(self._transcriptor.transcribe(file), new_filename, bucket_name)
        self._logger.info(f'Файл {filename} добавлен в хранилище')
        msg = {'filename': new_filename, 'bucket_name': bucket_name}
        self._rabbitmq_producer.send(json.dumps(msg).encode(), 'transcription_done')
        self._logger.info(f'Сообщение об успешной обработке {filename} отправлено')
