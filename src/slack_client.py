import os
from typing import List
import slack


class SlackClient:
    def __init__(self) -> None:
        self.slack_client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

    def send_code_to_slack(self, code: str) -> None:
        self.slack_client.chat_postMessage(
            channel='#shift-codes',
            text=code
        )

    def send_redemptions_to_slack(self, successful_submissions: List[str], failed_submissions: List[str]) -> None:
        success_message = f"Submission successful: {', '.join(successful_submissions)}\n" if successful_submissions else ''
        failure_message = f"Submission failure: {', '.join(failed_submissions)}" if failed_submissions else ''

        message = f"{success_message}{failure_message}"

        self.slack_client.chat_postMessage(
            channel='#shift-codes',
            text=message
    )

