import tempfile
from io import BytesIO


class WhisperTranscriptor:
    def __init__(self, model):
        self._model = model

    def transcribe(self, file: BytesIO) -> bytes:
        with tempfile.NamedTemporaryFile(suffix='.mp3') as tmp_file:
            tmp_file.write(file.read())
            tmp_file.flush()

            result = self._model.transcribe(tmp_file.name, language='ru')
            return result['text']
