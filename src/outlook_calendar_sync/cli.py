"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -moutlook_calendar_sync` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``outlook_calendar_sync.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``outlook_calendar_sync.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import logging
import os
import sys
from argparse import ArgumentParser

from outlook_calendar_sync.application import main
from outlook_calendar_sync.utils import log

parser = ArgumentParser("outlook-calendar-sync")
parser.add_argument("-n", type=int, help="Number of days in the future to sync", default=5)
parser.add_argument("--email", type=str, help="Outlook username to sync to")
parser.add_argument("--password", type=str, help="Outlook password")
parser.add_argument("--calendar-id", type=str, help="Google calendar ID to sync to")
parser.add_argument("--auth-code", type=str, help="Microsoft authenticator 2fa code. If not specified, will ask for input during execution")
parser.add_argument("--no-auth-code", action="store_true", help="Flag to set if no 2fa code is required, such as on a corporate network.")
parser.add_argument("--show-browser", action="store_true", default=False, help="Show the browser window")
args = parser.parse_args(sys.argv[1:])

username = args.email or os.getenv("OUTLOOK_USERNAME")
password = args.password or os.getenv("OUTLOOK_PASSWORD")
calendar_id = args.calendar_id or os.getenv("GCAL_CALENDAR_ID")

if hasattr(logging, (log_level := os.getenv("OUTLOOK_LOG_LEVEL", "INFO"))):
    log.setLevel(getattr(logging, log_level))
else:
    log.warning("Tried to set invalid log level %s, defaulting to INFO", log_level)
    log.setLevel(logging.INFO)

main(username, password, calendar_id, args)
