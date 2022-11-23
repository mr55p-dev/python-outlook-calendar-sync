import logging
import re
from datetime import datetime

app_log = logging.getLogger("application")


def find_event(tag):
    return tag.has_attr("aria-label") and "event from" in tag["aria-label"]


def get_event(detail: str):
    app_log.debug("Processing event with detail < %s >", detail)
    match = re.match(
        r'^(?:event from )(\w+), (\w+) (\d+), (\d+) ([\d:]+) to ([\d:]+) (.*?)(?: \w{0,3} )(?=location|organiser|recurring|event)(?#After 3 chars)(?:(?:location )(.*?)(?=organiser))?(?#after match location)(?:(?:organiser )(.*?)(?: recurring)?(?= event shown as))?(?#Ater match organiser)(?:(?:recurring)?(?: event shown as) (\w+))$(?#After match event transparency)', detail)
    if not match:
        app_log.error("Failed to parse event detail: '%s'", detail)
        return None

    day = match.group(1)
    month = match.group(2)
    date = match.group(3)
    year = match.group(4)
    start_time = match.group(5)
    end_time = match.group(6)

    summary = match.group(7)
    location = match.group(8)
    organiser = match.group(9)
    show_as = match.group(10)

    transparancy = "opaque" if show_as and show_as.lower() == "busy" else "transparent"

    start_timestamp = datetime.strptime(
        f"{day} {month} {date} {year} {start_time}", "%A %B %d %Y %H:%M")
    end_timestamp = datetime.strptime(
        f"{day} {month} {date} {year} {end_time}", "%A %B %d %Y %H:%M")

    event = {
        "summary": summary,
        "location": location,
        "organizer": {
            "displayName": organiser or "Ellis Lunnon",
            "self": "true" if not organiser else "false"
        },
        "transparency": transparancy,
        "start": {
            'dateTime': start_timestamp.isoformat(),
            'timeZone': "Europe/London"
        },
        "end": {
            'dateTime': end_timestamp.isoformat(),
            'timeZone': "Europe/London"
        }
    }
    app_log.debug("New event %s", summary)
    return event


def compare_events(g_event, o_event) -> bool:
    g_start = g_event['start'].get('dateTime', g_event['start'].get('date'))
    g_end = g_event['end'].get('dateTime', g_event['end'].get('date'))
    g_summary = g_event['summary']

    return g_start == o_event['start']['dateTime'] and g_end == o_event['end']['dateTime'] and g_summary == o_event['summary']
