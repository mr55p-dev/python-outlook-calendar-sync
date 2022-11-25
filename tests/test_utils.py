import pytest

from outlook_calendar_sync.utils import get_event

tests = [
    "event from Thursday, November 10, 2022 10:00 to 13:15 Good event name Vfb organiser Bill Gates recurring event shown as Busy",  # noqa: E501
    "event from Friday, November 18, 2022 01:00 to 04:00 Even better event  name Vfb organiser Elon Musk event shown as Busy",  # noqa: E501
    "event from Monday, November 13, 2022 10:30 to 11:00 Meeting to discuss leaving the EU Vfb organiser Nigel Farage event shown as Free",  # noqa: E501
    "event from Saturday, October 19, 2025 11:00 to 11:30 Reminder: Everything is awful Vfb location planet earth organiser Science event shown as Busy",  # noqa: E501
    "all day event from Saturday, October 19, 2025 to Sunday, October 27 Reminder: Everything is awful Vfb location planet earth organiser Science event shown as Busy",  # noqa: E501
]
responses = [
    {
        "summary": "Good event name",
        "location": None,
        "organizer": {"displayName": "Bill Gates", "self": "false"},
        "transparency": "opaque",
        "start": {"dateTime": "2022-11-10T10:00:00", "timeZone": "Europe/London"},
        "end": {"dateTime": "2022-11-10T13:15:00", "timeZone": "Europe/London"},
    },
    {
        "summary": "Even better event  name",
        "location": None,
        "organizer": {"displayName": "Elon Musk", "self": "false"},
        "transparency": "opaque",
        "start": {"dateTime": "2022-11-18T01:00:00", "timeZone": "Europe/London"},
        "end": {"dateTime": "2022-11-18T04:00:00", "timeZone": "Europe/London"},
    },
    {
        "summary": "Meeting to discuss leaving the EU",
        "location": None,
        "organizer": {"displayName": "Nigel Farage", "self": "false"},
        "transparency": "transparent",
        "start": {"dateTime": "2022-11-13T10:30:00", "timeZone": "Europe/London"},
        "end": {"dateTime": "2022-11-13T11:00:00", "timeZone": "Europe/London"},
    },
]


@pytest.mark.parametrize("test,response", zip(tests, responses))
def test_event_find(test, response):
    assert get_event(test) == response
