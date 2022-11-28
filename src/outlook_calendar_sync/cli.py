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
from argparse import ArgumentParser, Namespace

from outlook_calendar_sync.application import main as app
from outlook_calendar_sync.utils import (
    _init_config,
    default_config_path,
    load_config,
    log,
)


def app_handler(args: Namespace):
    config = load_config(args.config)
    config.read(args.config)

    username = args.email or config["OutlookCredentials"]["OutlookEmail"]
    password = args.password or config["OutlookCredentials"]["OutlookPassword"]
    calendar_id = args.calendar_id or config["GoogleCredentials"]["GoogleCalendarID"]
    calendar_uri = config.get("config", "outlookurl")
    log_level = config.get("config", "loglevel")
    requires_auth = config.getboolean("config", "requiresauthcode")
    days_to_fetch = int(args.n or config.get("config", "daystofetch"))
    page_load_delay = int(config.get("config", "pageloaddelay"))
    show_browser_window = args.show_browser

    auth_code = args.auth_code

    assert username
    assert password
    assert calendar_id

    if hasattr(logging, log_level):
        log.setLevel(getattr(logging, log_level))
    else:
        log.warning("Tried to set invalid log level %s, defaulting to INFO", log_level)
        log.setLevel(logging.INFO)

    app(
        username,
        password,
        calendar_id,
        calendar_uri,
        days_to_fetch=days_to_fetch,
        no_auth_code=requires_auth,
        auth_code=auth_code,
        page_load_delay=page_load_delay,
        show_browser_window=show_browser_window,
    )


def main():
    parser = ArgumentParser("outlook-calendar-sync")
    subp = parser.add_subparsers()
    init_parser = subp.add_parser("init", description="Setup the initial config file")
    init_parser.add_argument(
        "--path", help=f"Path to save the config file to (defaults to {default_config_path})", default=None, type=os.PathLike
    )
    init_parser.set_defaults(func=lambda arg: _init_config(arg.path))

    parser.add_argument("-n", type=int, help="Number of days in the future to sync", default=5)
    parser.add_argument(
        "--config", type=os.PathLike, help=f"Path to configuration file (defaults to {default_config_path})", default=default_config_path
    )
    parser.add_argument("--email", type=str, help="Outlook username to sync to")
    parser.add_argument("--password", type=str, help="Outlook password")
    parser.add_argument("--calendar-id", type=str, help="Google calendar ID to sync to")
    parser.add_argument(
        "--auth-code", type=str, help="Microsoft authenticator 2fa code. If not specified, will ask for input during execution"
    )
    parser.add_argument("--show-browser", action="store_true", default=False, help="Show the browser window")
    parser.set_defaults(func=app_handler)
    args = parser.parse_args(sys.argv[1:])
    args.func(args)


if __name__ == "__main__":
    main()
