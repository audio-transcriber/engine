import pika
from boto3 import client as boto3_client
from botocore.client import Config as BotoConfig
from dependency_injector import containers, providers
from dependency_injector.providers import Dependency

from infrastructure.minio import MinIOStorage
from infrastructure.rabbitmq import RabbitMQConsumer, RabbitMQProducer
from infrastructure.whisper import WhisperTranscriptor


class WhisperContainer(containers.DeclarativeContainer):
    model = Dependency()

    transcriptor = providers.Factory(WhisperTranscriptor, model)


class MinIOContainer(containers.DeclarativeContainer):
    endpoint_url = providers.Dependency()
    access_key = providers.Dependency()
    secret_key = providers.Dependency()

    client = providers.Factory(
        boto3_client,
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name='ru-central1',
        config=BotoConfig(signature_version='s3v4'),
    )
    storage = providers.Factory(MinIOStorage, client)


class RabbitMQContainer(containers.DeclarativeContainer):
    host = providers.Dependency()
    port = providers.Dependency()

    client = providers.Factory(
        pika.BlockingConnection,
        providers.Factory(
            pika.ConnectionParameters,
            host,
            port,
        ),
    )
    producer_client = providers.Resource(client)
    consumer_client = providers.Resource(client)
    producer = providers.Factory(RabbitMQProducer, producer_client)
    consumer = providers.Factory(RabbitMQConsumer, consumer_client)
