from typing import List

from src import orcicorn_client, shift_code_client, user_builder
from src.gcloud_storage import GCloudStorage
from src.slack_client import SlackClient
from src.user_builder import User


def redeem_codes(users: List[User], codes: List[str]):
    slack_client = SlackClient()
    for code in codes:
        print(code)
        slack_client.send_code_to_slack(code)
        submission_status = {
            'success': [],
            'failure': []
        }

        for user in users:
            try:
                shift_code_client.ShiftCodeClient(user, code).submit_shift_code()
                submission_status['success'].append(user.name)
            except Exception as e:
                print(e)
                submission_status['failure'].append(user.name)

        slack_client.send_redemptions_to_slack(submission_status['success'], submission_status['failure'])


def get_codes(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    storage_class = GCloudStorage()

    codes = orcicorn_client.get_new_codes(storage_class)
    if codes:
        users = user_builder.build_users(storage_class)
        redeem_codes(users, codes)

    return f'Found {len(codes)} code to submit. Check slack and shift for results!'


if __name__ == '__main__':
    get_codes(None)

