import sqlite3
from datetime import datetime, timedelta

# Connect to the database
conn = sqlite3.connect('secondbrain.db')  # Replace with your database name
cursor = conn.cursor()

cursor.execute("DELETE FROM meetings;")
cursor.execute("DELETE FROM processed_meetings_reminders;")
conn.commit()
conn.close()