import re

tests = [
        "event from Friday, November 18, 2022 10:00 to 10:15 Standup Banana Vfb organiser Alexsander Sebastiar recurring event shown as Busy",
        "event from Friday, November 18, 2022 10:15 to 10:30 Walkthrough  for CGB-2328 Vfb organiser Rohini Prashanth event shown as Busy",
        "event from Friday, November 18, 2022 10:30 to 11:00 Discussion over CGB-2263 Vfb organiser Ellis Lunnon event shown as Busy",
        "event from Friday, November 18, 2022 11:00 to 11:30 Reminder: Have you completed this weeks timesheet? Vfb location Planview. organiser Pam Biring event shown as Free",
]

for i in tests:
    match = re.match(r'^(event from )(\w+), (\w+) (\d+), (\d+) ([\d:]+) to ([\d:]+) (.*?) \w{3} (?=(?P<loc>location)|(?P<org>organiser))(?#After 3 chars)(?:(?:location )(.*?)(?=organiser))?(?#after match location)(?:(?:organiser )(.*?)(?: recurring)?(?= event shown as))?(?#Ater match organiser)(?:(?: event shown as) (\w+))$', i)
    if not match:
        print(i)
        continue

    day = match.group(1)
    month = match.group(2)
    year = match.group(4)
    date = match.group(3)
    start_time = match.group(5)
    end_time = match.group(6)

    summary = match.group(7)
    location = match.group(8)
    organiser = match.group(9)
    show_as = match.group(10)
