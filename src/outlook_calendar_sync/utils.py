import configparser
import logging
import re
from datetime import datetime
from os import PathLike
from pathlib import Path
from typing import TypeVar

log = logging.getLogger("application")
log.addHandler(logging.StreamHandler())
default_config_path = Path.home() / ".outlook-parser-config.ini"


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


def is_all_day(event) -> bool:
    """
    Check if an event is an all-day event.
    """
    return "dateTime" in event.get("start", {})


T = TypeVar("T")


def dedupe_events(events: list[T]) -> list[T]:
    unique_events = []
    for event in events:
        if event not in unique_events:
            unique_events.append(event)

    return unique_events


def _init_config(user_path: PathLike = None):
    if user_path:
        user_path = Path(user_path)
    else:
        user_path = default_config_path

    log.info("Setting up default configuration file at %s", str(user_path))

    config = configparser.ConfigParser()
    config["DEFAULT"] = {
        "daystofetch": 1,
        "loglevel": "INFO",
        "outlookurl": "https://outlook.office.com/calendar/view/day",
        "requiresauthcode": True,
        "pageloaddelay": 10,
        "self": "firstname lastname",
    }

    config["OutlookCredentials"] = {"OutlookEmail": "user.name@example.com", "OutlookPassword": "password123"}
    config["GoogleCredentials"] = {"GoogleCalendarID": "1234567890abcdef@group.calendar.google.com"}

    config["config"] = {"daystofetch": 1}

    with user_path.open("w") as f:
        config.write(f)


def load_config(config_file: PathLike = None):
    if not config_file:
        config_file = default_config_path
    log.debug("Reading config file from %s", str(config_file))
    config = configparser.ConfigParser()
    config.read(str(config_file))
    return config
