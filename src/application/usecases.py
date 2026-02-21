import json
from io import BytesIO
from pathlib import Path

from infrastructure.minio import MinIOStorage
from infrastructure.rabbitmq import RabbitMQProducer
from infrastructure.whisper import WhisperTranscriptor


class TranscriptionUseCase:
    def __init__(
        self,
        transcriptor: WhisperTranscriptor,
        storage: MinIOStorage,
        rabbitmq_producer: RabbitMQProducer,
    ) -> None:
        self._transcriptor = transcriptor
        self._storage = storage
        self._rabbitmq_producer = rabbitmq_producer

    def transcribe(self, filename: str, bucket_name: str) -> None:
        file = BytesIO(self._storage.get(filename, bucket_name))
        new_filename = Path(filename).with_suffix('.txt').name
        self._storage.save(self._transcriptor.transcribe(file), new_filename, bucket_name)
        msg = {'filename': filename}
        self._rabbitmq_producer.send(json.dumps(msg).encode(), 'transcription_done')
