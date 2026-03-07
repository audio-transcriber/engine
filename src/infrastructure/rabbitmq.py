import json
from typing import Callable

import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties


class RabbitMQProducer:
    def __init__(self, client: pika.BlockingConnection) -> None:
        self._client = client

    def send(self, msg: bytes, queue_name: str) -> None:
        with self._client.channel() as channel:
            channel.queue_declare(queue_name, durable=True)
            channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=msg,
            )


class RabbitMQConsumer:
    def __init__(self, client: pika.BlockingConnection) -> None:
        self._client = client

    def consume(self, queue_name: str, callback: Callable) -> None:
        with self._client.channel() as channel:
            channel.queue_declare(queue_name, durable=True)
            channel.basic_consume(queue_name, callback)
            channel.start_consuming()


def transcription_todo_callback(usecase: ...) -> Callable:  # TODO типизация
    def wrapper(ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes) -> None:
        try:
            data = json.loads(body.decode())
            usecase.transcribe(data['filename'], data['bucket_name'])
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception:
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    return wrapper
