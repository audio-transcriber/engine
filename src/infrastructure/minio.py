from contextlib import suppress

from boto3 import client as boto3_client


class MinIOStorage:
    def __init__(self, client: boto3_client) -> None:
        self._client = client

    def save(self, content: bytes, filename: str, bucket_name: str) -> None:
        with suppress(self._client.exceptions.BucketAlreadyOwnedByYou):
            self._client.create_bucket(Bucket=bucket_name)
        self._client.put_object(Bucket=bucket_name, Key=filename, Body=content)

    def get(self, filename: str, bucket_name: str) -> bytes:
        response = self._client.get_object(Bucket=bucket_name, Key=filename)
        body = response['Body']
        try:
            return body.read()
        finally:
            body.close()
