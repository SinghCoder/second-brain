import sqlite3
import threading
import time
from datetime import datetime, timedelta

from tools.slack import get_slack_message_link_from_ts, send_slack_dm


def fetch_meetings_within_next_hour():
    conn = sqlite3.connect('secondbrain.db')
    cursor = conn.cursor()

    while True:
        current_time = datetime.now()
        next_hour = current_time + timedelta(hours=1)

        query = "SELECT id as slack_message_ts, m.meeting_id, m.meeting_title as title, m.start_time, m.end_time FROM meetings m " \
                "LEFT JOIN processed_meetings_reminders p ON m.meeting_id = p.meeting_id " \
                "WHERE SUBSTR(m.start_time, 1, 16) BETWEEN SUBSTR(?, 1, 16) AND SUBSTR(?, 1, 16) AND p.meeting_id IS NULL;"
        cursor.execute(query, (current_time.astimezone().isoformat(), next_hour.astimezone().isoformat()))
        upcoming_meetings = cursor.fetchall()

        print("Upcoming meetings within the next hour:")
        messages = [{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"You have following meetings coming up in the next hour: \n\n"
            }
        }, {
            "type": "divider"
        }]
        for meeting in upcoming_meetings:
            slack_message_ts, meeting_id, title, start_time, end_time = meeting
            print(f"Title: {title}")
            print(f"Start Time: {start_time}")
            print(f"End Time: {end_time}")
            print("-" * 30)
            slack_message_link = get_slack_message_link_from_ts(slack_message_ts)
            message = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Title:* {title}\n*Start Time:* {start_time}\n*End Time:* {end_time}\n*Slack thread from which meeting was scheduled* {slack_message_link}"
                }
            }
            messages.append(message)
            messages.append({
                "type": "divider"
            })
            # Mark the meeting as processed in the 'processed_meetings' table
            cursor.execute("INSERT INTO processed_meetings_reminders (meeting_id) VALUES (?)", (meeting_id,))
            conn.commit()
        if len(upcoming_meetings) > 0:
            send_slack_dm("", blocks=messages)

        conn.commit()
        time.sleep(10)

    conn.close()

# Create a thread for continuous polling
polling_thread = threading.Thread(target=fetch_meetings_within_next_hour)
polling_thread.daemon = True  # Daemon threads will exit when the main program exits
polling_thread.start()

try:
    while True:
        pass  # Keep the main thread running
except KeyboardInterrupt:
    print("Exiting...")
