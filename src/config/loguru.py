from loguru import logger

logger.add(
    'logs/worker.log',
    format='{time} {level} {message}',
    filter=lambda record: record['extra'].get('service') == 'worker',
    rotation='00:00',
    retention='7 days',
    compression='zip',
)
logger.add(
    'logs/transcription.log',
    format='{time} {level} {message}',
    filter=lambda record: record['extra'].get('service') == 'transcription',
    rotation='00:00',
    retention='7 days',
    compression='zip',
)

worker_logger = logger.bind(service='worker')
transcription_logger = logger.bind(service='transcription')
