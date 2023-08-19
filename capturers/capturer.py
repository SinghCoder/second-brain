import os
import re
import traceback

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()
my_slack_user_name = "Harpinder Jot"
my_telegram_user_name = "SinghCoder"

slack_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

app = Flask(__name__)

def get_user_name(user_id):
    try:
        user_info = slack_client.users_info(user=user_id)
        return user_info['user']['real_name']
    except SlackApiError:
        print(f"Error getting user info: {traceback.format_exc()}")
        return user_id

def get_channel_name(channel_id):
    try:
        conversations = slack_client.conversations_list()
        for conversation in conversations['channels']:
            if conversation['id'] == channel_id:
                return conversation['name']
        return channel_id
    except SlackApiError:
        print(f"Error getting channel info: {traceback.format_exc()}")
        return channel_id


def resolve_mentions(message_text):
    user_mentions = re.findall(r'<@(\w+)>', message_text)
    resolved_message = message_text
    for mention in user_mentions:
        username = get_user_name(mention)
        resolved_message = resolved_message.replace(f'<@{mention}>', f'{username}')
    return resolved_message


@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json

    # Check if the request contains a challenge field
    if 'challenge' in data:
        return jsonify({"challenge": data['challenge']})

    event_type = data['event']['type']
    # Print only the message events:
    if event_type == 'message':
        user_id = data['event']['user']
        user_name = get_user_name(user_id)

        channel_id = data['event']['channel']
        channel_name = get_channel_name(channel_id)

        message_text = data['event']['text']
        resolved_message = resolve_mentions(message_text)

        # Format: User <user_name> sent message: <message_text> in channel <channel_name>
        content = f"User {user_name} sent message: {resolved_message} in channel {channel_name}"
        print(content)
        if my_slack_user_name in content:
            print("This message mentions me")

    # Respond to Slack to acknowledge receipt
    return jsonify({"status": "ok"})

@app.route('/telegram', methods=['POST'])
def telegram_events():
    data = request.json
    if 'message' in data and 'text' in data['message']:
        username = data['message']['from']['first_name']
        text = data['message'].get("text", "No text")

        content = f"User {username} sent message: {text}"
        print(content)
        if my_telegram_user_name in content:
            print("This message mentions me")
        return jsonify({"message": "Event received"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
