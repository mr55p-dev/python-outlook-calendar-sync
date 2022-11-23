# Usage

- Install selenium driver to /usr/local/bin/chromedriver
- Install dependencies (optionally create a `venv` first) with `pip install -r requirements.txt`
- Install the CLI tool with `pip install .`
- Run the tool using `outlook-calendar-sync` (help is available with the `-h` flag)
- Set the outlook username and password and target calendar either as CLI args or through environment variables:
  - OUTLOOK_USERNAME
  - OUTLOOK_PASSWORD
  - GCAL_CALENDAR_ID


# Todo
- [ ] Create some error handling for the outlook sign up process
  - [ ] Exception on invalid username
  - [ ] Exception on invalid password
  - [ ] Exception on invalid auth code
- [ ] Handle the case where authenticator is not required (either auto detect or use flag)
- [ ] Switch from using css selectors to XPath
- [ ] Put dependencies in the setuptools script

