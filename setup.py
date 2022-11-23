import setuptools

setuptools.setup(
    name='outlook-calendar-sync',
    version='0.1',
      description='Sync private outlook calendars to GCal',
      author='Ellis Lunnon',
      author_email='ellislunnon@gmail.com',
      url='https://www.example.com',
      packages=['outlook_calendar_sync'],
      install_requires=[
        "selenium",
        "beautifulsoup4",
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
      ],
      entry_points={
        "console_scripts": [
            "outlook-calendar-sync=outlook_calendar_sync.sync:cli"
        ]
      }
)
