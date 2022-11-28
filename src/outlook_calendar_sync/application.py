from datetime import datetime, timedelta

from outlook_calendar_sync.gcal import (
    find_incorrect_gcal_events,
    find_new_outlook_events,
    get_gcal_api,
    update_calendar,
)
from outlook_calendar_sync.outlook import (
    get_selenium_driver,
    outlook_login,
    outlook_select_page_events,
)
from outlook_calendar_sync.utils import dedupe_events, log


def main(
    username: str,
    password: str,
    calendar_id: str,
    calendar_uri: str,
    days_to_fetch: int = 1,
    page_load_delay: int = 10,
    show_browser_window: bool = False,
    auth_code: str = "",
    no_auth_code: bool = False,
):
    """Application logic to open a browser session, collect events, parse them
    and synchronise them with a google calendar.

    Args:
        username (str): outlook username
        password (str): outlook password
        calendar_id (str): google calendar id
        args (argparse): additional arguments to access
    """
    #  Define what window we are updating
    window_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"
    window_end = (datetime.now() + timedelta(days=days_to_fetch - 1)).replace(
        hour=23, minute=59, second=59, microsecond=0
    ).isoformat() + "Z"
    log.info("Scanning events between %s and %s", window_start, window_end)

    # Set up the driver
    driver = get_selenium_driver(show_browser_window)
    calendar_session = outlook_login(driver, username, password, calendar_uri, auth_code=auth_code, no_auth_code=no_auth_code)
    log.debug("Outlook session created")

    # Get the outlook events into gcal form
    events_iter = outlook_select_page_events(calendar_session, days=days_to_fetch, delay=page_load_delay)
    outlook_events = [j for i in events_iter for j in i if i if j]
    log.debug("Collected %d events", len(outlook_events))

    # Deduplicate all day events
    outlook_events = dedupe_events(outlook_events)
    log.debug("%d events remain after deduplication", len(outlook_events))

    # Setup the google api service
    service = get_gcal_api()

    # Create a new calendar
    if not calendar_id:
        new_cal = service.calendars().insert(body={"summary": "Outlook (synchronised)"}).execute()
        calendar_id = new_cal["id"]
        log.info("Created new google calendar (id %s)", calendar_id)

    # Get the events on the calendar
    events_result = (
        service.events()
        .list(calendarId=calendar_id, timeMin=window_start, timeMax=window_end, singleEvents=True, orderBy="startTime")
        .execute()
    )
    gcal_events = events_result.get("items", []) or []

    # Prints the start and name of the next 10 events
    new_events = find_new_outlook_events(outlook_events, gcal_events)
    outdated_events = find_incorrect_gcal_events(outlook_events, gcal_events)

    update_calendar(service, calendar_id, new_events, outdated_events)
