import sqlite3

# Connect to or create a new database file called "secondbrain.db"
conn = sqlite3.connect('secondbrain.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS meetings (
        id TEXT PRIMARY KEY,     -- This would be the ID of the corresponding source from which the meeting was created. So, for Slack, this would be the parent Slack message ID.
        meeting_id TEXT NOT NULL -- This would be the ID of the meeting in the calendar.
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS slack_messages (
        message_id TEXT PRIMARY KEY
    )
''')
conn.commit()

def store_slack_message(message_id: str) -> None:
    conn = sqlite3.connect('secondbrain.db')
    cursor = conn.cursor()
    # IF it already exists, then don't do anything
    if slack_message_exists(message_id):
        return
    cursor.execute('INSERT INTO slack_messages VALUES (?)', (message_id,))
    conn.commit()
    conn.close()

def slack_message_exists(message_id: str) -> bool:
    conn = sqlite3.connect('secondbrain.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM slack_messages WHERE message_id=?', (message_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return True
    else:
        return False

def create_meeting(source_id: str, meeting_id: str) -> None:
    conn = sqlite3.connect('secondbrain.db')
    cursor = conn.cursor()
    print(f"Creating meeting with source_id: {source_id} and meeting_id: {meeting_id}")
    cursor.execute('INSERT INTO meetings VALUES (?, ?)', (source_id, meeting_id))
    conn.commit()
    # Print all the rows in the table
    cursor.execute('SELECT * FROM meetings')
    print(cursor.fetchall())
    conn.close()

def get_meeting_id_from_source_id(source_id: str) -> tuple[str, bool]:
    conn = sqlite3.connect('secondbrain.db')
    cursor = conn.cursor()
    cursor.execute('SELECT meeting_id FROM meetings WHERE id=?', (source_id,))
    meeting_id = cursor.fetchone()
    conn.close()
    if meeting_id:
        return meeting_id[0], True
    else:
        return "", False

def print_all_meetings() -> None:
    cursor.execute('SELECT * FROM meetings')
    print(cursor.fetchall())

# if __name__ == '__main__':
#     print_all_meetings()
