import logging
import os
import sys
from argparse import ArgumentParser
from datetime import datetime, timedelta

from outlook_calendar_sync.gcal import (find_incorrect_gcal_events,
                                        find_new_outlook_events, get_gcal_api,
                                        update_calendar)
from outlook_calendar_sync.outlook import (get_selenium_driver, outlook_login,
                                           outlook_select_page_events)


app_log = logging.getLogger("application")


def main(username, password, calendar_id, args):
    delay = 7

    #  Define what window we are updating
    window_start = datetime.now().replace(hour=0, minute=0, second=0,
                                          microsecond=0).isoformat() + 'Z'
    window_end = (datetime.now() + timedelta(days=args.n-1)
                  ).replace(hour=23, minute=59, second=59, microsecond=0).isoformat() + 'Z'
    app_log.info("Scanning events between %s and %s", window_start, window_end)

    # Set up the driver
    driver = get_selenium_driver(args.debug)
    calendar_session = outlook_login(
        driver, username, password, auth_code=args.auth_code)
    app_log.debug("Outlook session created")

    # Get the outlook events into gcal form
    events_iter = outlook_select_page_events(
        calendar_session, days=args.n, delay=delay)
    outlook_events = [j for i in events_iter for j in i if i if j]
    app_log.debug(outlook_events)

    # Setup the google api service
    service = get_gcal_api()

    # Create a new calendar
    if not calendar_id:
        new_cal = service.calendars().insert(
            body={"summary": "Outlook (synchronised)"}).execute()
        calendar_id = new_cal['id']
        app_log.info("Created new google calendar (id %s)", calendar_id)

    # Get the events on the calendar
    events_result = service.events().list(calendarId=calendar_id,
                                          timeMin=window_start,
                                          timeMax=window_end,
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    gcal_events = events_result.get('items', []) or []

    # Prints the start and name of the next 10 events
    new_events = find_new_outlook_events(outlook_events, gcal_events)
    outdated_events = find_incorrect_gcal_events(outlook_events, gcal_events)

    update_calendar(service, calendar_id, new_events, outdated_events)


def cli():
    parser = ArgumentParser("outlook-calendar-sync")
    parser.add_argument(
        "-n", type=int, help="Number of days in the future to sync", default=5)
    parser.add_argument("--email", type=str,
                        help="Outlook username to sync to")
    parser.add_argument("--password", type=str, help="Outlook password")
    parser.add_argument("--calendar-id", type=str,
                        help="Google calendar ID to sync to")
    parser.add_argument("--auth-code", type=str,
                        help="Microsoft authenticator 2fa code. If not specified, will ask for input during execution")
    parser.add_argument("--debug", action="store_true",
                        default=False, help="Run the browser using a head")
    args = parser.parse_args(sys.argv[1:])

    username = args.email or os.getenv("OUTLOOK_USERNAME")
    password = args.password or os.getenv("OUTLOOK_PASSWORD")
    calendar_id = args.calendar_id or os.getenv("GCAL_CALENDAR_ID")

    assert username
    assert password
    assert calendar_id

    logging.getLogger("application").setLevel(
        logging.DEBUG if args.debug else logging.INFO)

    main(username, password, calendar_id, args)

    # calendar_id = 'hta5jrkqf8hos4pell5h8un0vs@group.calendar.google.com'


if __name__ == "__main__":
    cli()
