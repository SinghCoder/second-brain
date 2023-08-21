import sqlite3
from datetime import datetime, timedelta

# Connect to the database
conn = sqlite3.connect('secondbrain.db')  # Replace with your database name
cursor = conn.cursor()

cursor.execute("DELETE FROM meetings;")
cursor.execute("DELETE FROM processed_meetings_reminders;")
conn.commit()

# Define the current datetime and next 3 hours
current_time = datetime.now()
next_3_hours = current_time + timedelta(hours=3)

# Sample meeting data
meetings = [
    ("1692461778.500409", "mid1", "Meeting 1", (current_time + timedelta(minutes=10)).astimezone().isoformat(), (current_time + timedelta(minutes=30)).astimezone().isoformat()),
    ("1692597573.997689", "mid2", "Meeting 2", (current_time + timedelta(minutes=45)).astimezone().isoformat(), (current_time + timedelta(minutes=60)).astimezone().isoformat()),
    ("1692461715.396249", "mid3", "Meeting 3", (current_time + timedelta(minutes=90)).astimezone().isoformat(), (current_time + timedelta(minutes=120)).astimezone().isoformat()),
    ("1692450769.600659", "mid4", "Meeting 4", (current_time + timedelta(minutes=150)).astimezone().isoformat(), (current_time + timedelta(minutes=180)).astimezone().isoformat()),
]

# Insert sample meeting data into the 'meetings' table
for meeting in meetings:
    cursor.execute("INSERT INTO meetings (id, meeting_id, meeting_title, start_time, end_time) VALUES (?, ?, ?, ?, ?)", meeting)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Sample meeting data inserted.")
