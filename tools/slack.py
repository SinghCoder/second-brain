import os
from slack_sdk import WebClient
from langchain.tools import tool

from dotenv import load_dotenv
load_dotenv()

slack_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
slack_user_id = os.environ.get("SLACK_USER_ID")

def send_slack_message(channel_id, message):
    try:
        resp = slack_client.chat_postMessage(channel=channel_id, text=message)
    except Exception as e:
        print(f"Error sending slack message: {e}")
        return {"error": {e}}
    return None

@tool
def notify_user(message):
    """
    Send a message to the user
    """
    return send_slack_message(channel_id=slack_user_id, message=message)
