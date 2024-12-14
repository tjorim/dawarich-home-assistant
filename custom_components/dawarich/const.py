"""Constants for the Dawarich integration."""

from datetime import timedelta

DOMAIN = "dawarich"


DEFAULT_PORT = 80
DEFAULT_NAME = "Dawarich"
DEFAULT_LOCATION = "Home"
DEFAULT_SSL = False
DEFAULT_VERIFY_SSL = True
CONF_DEVICE = "mobile_app"
UPDATE_INTERVAL = timedelta(seconds=20)
