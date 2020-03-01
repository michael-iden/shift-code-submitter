from src import orcicorn_client, slack_client, shift_code_client, user_builder
from src.gcloud_storage import GCloudStorage

storage_class = GCloudStorage()


def redeem_code(shift_code):
    successful_submissions = []
    failed_submissions = []

    for user in user_builder.build_users(storage_class):
        try:
            shift_code_client.ShiftCodeClient(user, shift_code).submit_shift_code()
            successful_submissions.append(user.name)
        except Exception as e:
            print(e)
            failed_submissions.append(user.name)

    slack_client.send_redemptions_to_slack(successful_submissions, failed_submissions)


def get_codes(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

    codes = orcicorn_client.get_new_codes(storage_class)
    for code in codes:
        print(code)
        slack_client.send_code_to_slack(code)
        redeem_code(code)

    return f'Found {len(codes)} code to submit. Check slack and shift for results!'


if __name__ == '__main__':
    get_codes(None)

