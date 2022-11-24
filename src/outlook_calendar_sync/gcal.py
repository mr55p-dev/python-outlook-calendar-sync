import logging
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from outlook_calendar_sync.utils import compare_events

app_log = logging.getLogger("application")

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_gcal_api():
    # Setup google calendar integration
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if Path("./token.json").exists():
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


def find_new_outlook_events(outlook_events, gcal_events):
    new_events = []
    # Find all newly discovered events
    for o_event in outlook_events:
        event_in_gcal = False

        for g_event in gcal_events:
            if compare_events(g_event, o_event):  # events match
                event_in_gcal = True
                break

        if not event_in_gcal:
            new_events.append(o_event)

    app_log.info("Found %d events to add", len(new_events))

    return new_events


def find_incorrect_gcal_events(outlook_events, gcal_events):
    incorrect_events = []
    # Remove any events not found in outlook
    for g_event in gcal_events:
        event_in_outlook = False

        for o_event in outlook_events:
            if compare_events(g_event, o_event):  # Events match
                event_in_outlook = True
                break

        if not event_in_outlook:
            incorrect_events.append(g_event)

    app_log.info("Found %d events to remove", len(incorrect_events))

    return incorrect_events


def update_calendar(service, calendar_id, events_to_add, events_to_remove):
    # perform updates
    for g_event in events_to_remove:
        service.events().delete(calendarId=calendar_id, eventId=g_event["id"]).execute()

    for o_event in events_to_add:
        service.events().insert(calendarId=calendar_id, body=o_event).execute()
