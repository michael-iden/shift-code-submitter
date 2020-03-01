import os

from google.cloud import storage
from google.cloud.storage import Blob


class GCloudStorage:

    def __init__(self) -> None:
        self.bucket_name = os.environ['GCLOUD_BUCKET_NAME']
        self.creds_folder_name = os.environ.get('GCLOUD_CREDS_FOLDER_NAME', 'creds')
        self.last_timestamp_filename = os.environ.get('GCLOUD_LAST_TIMESTAMP_FILENAME', 'last_timestamp.txt')

        self.client = storage.Client()
        self.bucket = self.client.get_bucket(self.bucket_name)
        self.timestamp_blob = self.bucket.get_blob(self.last_timestamp_filename) or self.__create_new_timestamp_blob()

    def __create_new_timestamp_blob(self):
        blob = Blob(self.last_timestamp_filename, self.bucket)
        blob.upload_from_string('0')
        return blob

    def get_users(self):
        blobs = self.client.list_blobs(self.bucket, prefix=self.creds_folder_name)
        return [blob.download_as_string().decode("utf-8").split("\n") for blob in blobs]

    def set_latest_timestamp(self, lasted_timestamp: str):
        self.timestamp_blob.upload_from_string(lasted_timestamp)

    def get_latest_timestamp(self) -> float:
        return float(self.timestamp_blob.download_as_string())
