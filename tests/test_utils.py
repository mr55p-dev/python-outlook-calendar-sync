from outlook_calendar_sync.utils import get_event


def test_event_parsing():
    tests = [
        "all day event from Wednesday, November 23, 2022 to Friday, November 25, 2022 Nil A/L meb organiser Nil Bozkurt event shown as Free",  # noqa: E501
        "event from Friday, November 18, 2022 10:00 to 10:15 Standup Banana Vfb organiser Alexsander Sebastiar recurring event shown as Busy",  # noqa: E501
        "event from Friday, November 18, 2022 10:15 to 10:30 Walkthrough  for CGB-2328 Vfb organiser Rohini Prashanth event shown as Busy",  # noqa: E501
        "event from Friday, November 18, 2022 10:30 to 11:00 Discussion over CGB-2263 Vfb organiser Ellis Lunnon event shown as Busy",  # noqa: E501
        "event from Friday, November 18, 2022 11:00 to 11:30 Reminder: Have you completed this weeks timesheet? Vfb location Planview. organiser Pam Biring event shown as Free",  # noqa: E501
    ]
    results = []
    for detail, result in zip(tests, results):
        assert get_event(detail) == result
