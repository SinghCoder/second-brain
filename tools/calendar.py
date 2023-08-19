from datetime import datetime
from typing import Any, List

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from langchain.tools import tool

from oauth.google import get_google_oauth_creds

## Google Calendar API 
## https://developers.google.com/calendar/api/v3/reference

@tool
def create_calendar_event(title: str, start_time: datetime, end_time: datetime, invitees: List[str]) -> str:
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
            'description': 'From slack message from harpinder.',
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
        return "Event successfully created. Do not create again. Stop now."

    except HttpError as error:
        return f"Event creation failed due to an error {error}"

@tool
def get_calendar_events() -> List[Any]:
    """
        Returns list of calendar events for the user for the current day.
    """

    creds = get_google_oauth_creds()
    if creds is None:
        raise Exception("No credentials found")

    try:
        service = build('calendar', 'v3', credentials=creds)
        page_token = None
        today = datetime.utcnow().date().isoformat()
        events = []
        while True:
            events_result = service.events().list(
                calendarId='primary',
                timeMin=today + 'T00:00:00Z',
                timeMax=today + 'T23:59:59Z',
                singleEvents=True,
                orderBy='startTime',
                pageToken=page_token
            ).execute()
            events.extend(events_result.get('items', []))
            page_token = events_result.get('nextPageToken')
            if not page_token:
                break
    except HttpError as error:
        print(f"An error occurred: {error}")
        raise HttpError
    if not events:
        print("No events found for today")
        return "No events found for today"
    else:
        returnVal = ""
        print('Events for today:')
        returnVal += 'Events for today:\n'
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            print(f"{start} - {end} - {event['summary']}")
            returnVal += f"{start} - {end} - {event['summary']}\n"
        return returnVal

