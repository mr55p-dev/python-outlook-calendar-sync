import logging
import re
from datetime import datetime

log = logging.getLogger("application")


def find_event(tag):
    return tag.has_attr("aria-label") and "event from" in tag["aria-label"]


def get_event(detail: str):
    log.debug("Processing event with detail < %s >", detail)
    match = re.match(
        r"^(all day )?(?:event from )(\w+), (\w+) (\d+), (\d+) (?:([\d:]+))?\s?to (?:(\w+), (\w+) (\d+), (\d+))?(?:([\d:]+))? (.*)(?: \w{0,3} )(?=location|organiser|recurring|event)(?#After 3 chars)(?:(?:location )(.*?)(?=organiser))?(?#after match location)(?:(?:organiser )(.*?)(?: recurring)?(?= event shown as))?(?#Ater match organiser)(?:(?:recurring)?(?: event shown as) (\w+))$(?#After match event transparency)",  # noqa
        detail,
    )
    if not match:
        log.error("Failed to parse event detail: '%s'", detail)
        return None

    start_day = match.group(2)
    start_month = match.group(3)
    start_date = match.group(4)
    start_year = match.group(5)

    # If an all day event
    if match.group(1):
        end_day = match.group(7)
        end_month = match.group(8)
        end_date = match.group(9)
        end_year = match.group(10)

        start_timestamp = datetime.strptime(f"{start_day} {start_month} {start_date} {start_year}", "%A %B %d %Y")
        end_timestamp = datetime.strptime(f"{end_day} {end_month} {end_date} {end_year}", "%A %B %d %Y")

        start = {"date": start_timestamp.strftime("%Y-%m-%d"), "timeZone": "Europe/London"}
        end = {"date": end_timestamp.strftime("%Y-%m-%d"), "timeZone": "Europe/London"}
    else:
        start_time = match.group(6)
        end_time = match.group(11)
        start_timestamp = datetime.strptime(f"{start_day} {start_month} {start_date} {start_year} {start_time}", "%A %B %d %Y %H:%M")
        end_timestamp = datetime.strptime(f"{start_day} {start_month} {start_date} {start_year} {end_time}", "%A %B %d %Y %H:%M")

        start = {"dateTime": start_timestamp.isoformat(), "timeZone": "Europe/London"}
        end = {"dateTime": end_timestamp.isoformat(), "timeZone": "Europe/London"}

    summary = match.group(12)
    location = match.group(13)
    organiser = match.group(14)
    show_as = match.group(15)

    transparancy = "opaque" if show_as and show_as.lower() == "busy" else "transparent"

    event = {
        "summary": summary,
        "location": location,
        "organizer": {"displayName": organiser or "Ellis Lunnon", "self": "true" if not organiser else "false"},
        "transparency": transparancy,
        "start": start,
        "end": end,
    }
    log.debug("New event %s", summary)
    return event


def compare_events(g_event, o_event) -> bool:
    return g_event == o_event
