import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from langchain.tools import tool
from datetime import datetime

from oauth.google import get_google_oauth_creds

## Google Calendar API 
## https://developers.google.com/calendar/api/v3/reference

@tool
def create_calendar_event(title: str, start_time: datetime, end_time: datetime, invitees: list[str]) -> str:
    """
        Creates a Google Calendar event for the user with the given title, start time, and end time.
        It also invites the invitees (which is list of emails).
        Returns the event ID of the created event.
    """
    
    creds = get_google_oauth_creds()
    if creds is None:
        raise Exception("No credentials found")
    
    print("Creating event")
    print(f"Title: {title}")
    print(f"Start time: {start_time.astimezone().isoformat()}")
    print(f"End time: {end_time.astimezone().isoformat()}")
    print(f"Invitees: {invitees}")

    try:
        service = build('calendar', 'v3', credentials=creds)
        attendees = [{'email': email} for email in invitees]
        event = {
            'summary': title,
            'description': 'From slack message from harpinder',
            'start': {
                'dateTime': start_time.astimezone().isoformat(),
            },
            'end': {
                'dateTime': end_time.astimezone().isoformat(),
            },
            'attendees': attendees,
            'reminders': {
                'useDefault': True,
            },
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
        print(event)
        if event is None:
            raise Exception("Event creation failed")
        print("Event successfully created")
        return 

    except HttpError as error:
        print(f"An error occurred: {error}")
        raise HttpError

