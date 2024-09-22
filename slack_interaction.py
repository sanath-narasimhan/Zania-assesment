import os
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from config import Config

logger = logging.getLogger(__name__)

class SlackClient:
    def __init__(self):
        self.client = WebClient(token=Config.SLACK_TOKEN)

    def post_message(self, message):
        """
        Post a message to a Slack channel.

        Args:
            message (str): The message to post on Slack.

        Returns:
            None
        """
        try:
            response = self.client.chat_postMessage(
                channel=Config.SLACK_CHANNEL,
                text=message
            )
            logger.info(f"Message posted to Slack channel {Config.SLACK_CHANNEL}: {message}")
        except SlackApiError as e:
            logger.error(f"Failed to post message to Slack: {e.response['error']}")
            raise