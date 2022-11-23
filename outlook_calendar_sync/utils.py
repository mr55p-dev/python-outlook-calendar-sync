import logging
import re
from datetime import datetime

app_log = logging.getLogger("application")


def find_event(tag):
    return tag.has_attr("aria-label") and "event from" in tag["aria-label"]


def get_event(detail: str):
    app_log.debug("Processing event with detail < %s >", detail)
    print(detail)
    match = re.match(
        r'^(all day )?(?:event from )(\w+), (\w+) (\d+), (\d+) (?:([\d:]+))?\s?to (?:(\w+), (\w+) (\d+), (\d+))?(?:([\d:]+))? (.*)(?: \w{0,3} )(?=location|organiser|recurring|event)(?#After 3 chars)(?:(?:location )(.*?)(?=organiser))?(?#after match location)(?:(?:organiser )(.*?)(?: recurring)?(?= event shown as))?(?#Ater match organiser)(?:(?:recurring)?(?: event shown as) (\w+))$(?#After match event transparency)', detail)
    if not match:
        app_log.error("Failed to parse event detail: '%s'", detail)
        return None

    # Handle all day event
    all_day = bool(match.group(1))

    start_day = match.group(2)
        


    start_day = match.group(2)
    start_month = match.group(3)
    start_date = match.group(4)
    start_year = match.group(5)

    # If an all day event
    if match.group(1):
        end_day = match.group(7)
        end_month = match.group(8)
        end_date = match.group(9)
        end_year = match.group(10)

        start_timestamp = datetime.strptime(
            f"{start_day} {start_month} {start_date} {start_year}", "%A %B %d %Y")
        end_timestamp = datetime.strptime(
            f"{end_day} {end_month} {end_date} {end_year}", "%A %B %d %Y")

        start = {
            "date": start_timestamp.strftime("%Y-%m-%d"),
            'timeZone': "Europe/London"
        }
        end = {
            "date": end_timestamp.strftime("%Y-%m-%d"),
            'timeZone': "Europe/London"
        }
        print(start)
        print(end)
    else:
        start_time = match.group(6)
        end_time = match.group(11)
        start_timestamp = datetime.strptime(
            f"{start_day} {start_month} {start_date} {start_year} {start_time}", "%A %B %d %Y %H:%M")
        end_timestamp = datetime.strptime(
            f"{start_day} {start_month} {start_date} {start_year} {end_time}", "%A %B %d %Y %H:%M")

        start = {
            'dateTime': start_timestamp.isoformat(),
            'timeZone': "Europe/London"
        }
        end = {
            'dateTime': end_timestamp.isoformat(),
            'timeZone': "Europe/London"
        }

    summary = match.group(12)
    location = match.group(13)
    organiser = match.group(14)
    show_as = match.group(15)

    transparancy = "opaque" if show_as and show_as.lower() == "busy" else "transparent"


    event = {
        "summary": summary,
        "location": location,
        "organizer": {
            "displayName": organiser or "Ellis Lunnon",
            "self": "true" if not organiser else "false"
        },
        "transparency": transparancy,
        "start": start,
        "end": end
    }
    app_log.debug("New event %s", summary)
    return event


def compare_events(g_event, o_event) -> bool:
    return g_event == o_event
    # g_start = g_event['start'].get('dateTime', g_event['start'].get('date'))
    # g_end = g_event['end'].get('dateTime', g_event['end'].get('date'))
    # g_summary = g_event['summary']
    #
    # return g_start == o_event['start']['dateTime'] and g_end == o_event['end']['dateTime'] and g_summary == o_event['summary']
