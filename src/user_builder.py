from dataclasses import dataclass

from src.gcloud_storage import GCloudStorage


def build_users(storage_class: GCloudStorage):
    user_data_list = storage_class.get_users()
    return [User(user_data[0], user_data[1], user_data[2]) for user_data in user_data_list]


@dataclass
class User:
    name: str
    email: str
    password: str
