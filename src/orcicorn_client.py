import datetime

from src.gcloud_storage import GCloudStorage
from src.orcicorn_service import OrcicornService


def get_code_timestamp(code):
    return datetime.datetime.strptime(code.get('archived'), '%d %b %Y %H:%M:%S %z').timestamp()


def get_new_codes(storage_class: GCloudStorage):
    response = OrcicornService.bl3_codes()[0]

    last_checked_timestamp = storage_class.get_latest_timestamp()
    codes_to_submit = [code.get('code') for code in response.get('codes', []) if get_code_timestamp(code) > last_checked_timestamp]
    storage_class.set_latest_timestamp(response.get('meta', {}).get('generated', {}).get('epoch'))

    return codes_to_submit
