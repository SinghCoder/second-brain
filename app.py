import os
import re
import time
import traceback
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from urlextract import URLExtract

from db import get_meeting_id_from_source_id, slack_message_exists, store_slack_message
from distill import distill_agent_executor
from organize import organize_agent_executor
from qna import qna
from tools.calendar import update_meeting_body
from tools.slack import send_message_in_thread

NUM_THREADS = 1
executor = ThreadPoolExecutor(max_workers=NUM_THREADS)

load_dotenv()

SLACK_USERNAME = os.environ.get("SLACK_USERNAME")
TELEGRAM_USER_NAME = os.environ.get("TELEGRAM_USERNAME")

slack_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
organize_agent = organize_agent_executor()
distill_agent = distill_agent_executor()

def organize(content):
    executor.submit(organize_agent.run, content)

def distill(content):
    executor.submit(distill_agent.run, content)

app = Flask(__name__)

def get_user_info(user_id):
    try:
        user_info = slack_client.users_info(user=user_id)
        is_bot = user_info['user']['is_bot']
        user_name = user_info['user']['real_name']
        user_email = ""
        if not is_bot:
            user_email = user_info['user']['profile']['email']
        return is_bot, user_name, user_email
    except SlackApiError:
        print(f"Error getting user info: {traceback.format_exc()}")
        return user_id, ""

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
        is_bot, user_name, user_email = get_user_info(mention)
        if is_bot:
            return is_bot, resolved_message.replace(f'<@{mention}>', '')
        resolved_message = resolved_message.replace(f'<@{mention}>', f'{user_name} - {user_email}')
    return False, resolved_message


@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json
    print(data)

    # Check if the request contains a challenge field
    if 'challenge' in data:
        return jsonify({"challenge": data['challenge']})

    event_data = data['event']
    event_type = event_data['type']

    if event_type != 'message':
        print(f"Event type {event_type} not supported")
        return jsonify({"status": "ok"})

    ts = event_data['event_ts']
    if slack_message_exists(ts):
        print(f"Message with ts: {ts} already exists. Ignoring.")
        return jsonify({"status": "ok"})
    else:
        store_slack_message(ts)
    
    user_id = event_data['user']
    is_bot, user_name, user_email = get_user_info(user_id)
    channel_id = event_data['channel']
    channel_name = get_channel_name(channel_id)
    thread_ts = event_data.get('thread_ts', "")
    message_text = event_data['text']
    is_bot_message, resolved_message = resolve_mentions(message_text)
    if is_bot_message:
        send_message_in_thread(channel_id, ts, qna(resolved_message))
        return jsonify({"status": "ok"})

    content = f"{ts} | User {user_name}({user_email}): {resolved_message}"
    print(content)
    meeting_id, exists = get_meeting_id_from_source_id(thread_ts)
    if exists:
        update_meeting_body(meeting_id, resolved_message)
        organize(content)
    if not exists:
        concerned_message = SLACK_USERNAME in content
        if concerned_message:
            organize(content)
            distill("Notify the user if there is any conflicting events.")
    return jsonify({"status": "ok"})

@app.route('/telegram', methods=['POST'])
def telegram_events():
    data = request.json
    print(data)
    if 'message' in data and 'text' in data['message']:
        username = data['message']['from']['first_name']
        text = data['message'].get("text", "No text")

        content = f"User {username} sent message on telegram: {text}"
        print(content)
        if TELEGRAM_USER_NAME in content.lower():
            print("This message mentions me")
            organize(content)
        return jsonify({"message": "Event received"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
    # wait for the executor to finish
    executor.shutdown()
