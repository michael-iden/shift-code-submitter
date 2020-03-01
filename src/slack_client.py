import os
from typing import List
import slack

slack_client = slack.WebClient(token=os.environ['SLACK_TOKEN'])


def send_code_to_slack(code: str) -> None:
    slack_client.chat_postMessage(
        channel='#shift-codes',
        text=code
    )


def send_redemptions_to_slack(successful_submissions: List[str], failed_submissions: List[str]) -> None:
    success_message = f"Submission successful: {', '.join(successful_submissions)}\n" if successful_submissions else ''
    failure_message = f"Submission failure: {', '.join(failed_submissions)}" if failed_submissions else ''

    message = f"{success_message}{failure_message}"

    slack_client.chat_postMessage(
        channel='#shift-codes',
        text=message
    )

