"""Dawarich integration."""

from logging import getLogger
import random
import time

from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Event, EventStateChangedData, HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.typing import ConfigType

from . import DOMAIN
from .dawarich_api import DawarichAPI

_LOGGER = getLogger(__name__)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info=None,
) -> None:
    """Set up the sensor platform."""
    async_add_entities([DawarichSensor(entry=config, hass=hass)])


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities([DawarichSensor(entry=config_entry.data, hass=hass)])


class DawarichSensor(TrackerEntity):
    """Dawarich Sensor Class."""

    def __init__(self, entry: ConfigType, hass: HomeAssistant) -> None:
        """Initialize the sensor."""
        self._friendly_name = entry["friendly_name"]
        self._url = entry["url"]
        self._api_key = entry["api_key"]
        self._mobile_app = entry["mobile_app"]

        self._latitude = 0.0
        self._longitude = 0.0
        self._location_name = "Home"
        self._location_accuracy = 2

        self._api = DawarichAPI(
            url=self._url, api_key=self._api_key, name=self._friendly_name
        )

        self._hass = hass
        self._async_unsubscribe_state_changed = async_track_state_change_event(
            hass=self._hass,
            entity_ids=[self._mobile_app],
            action=self._get_state_change,
        )

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._friendly_name

    @property
    def latitude(self) -> float:
        """Return latitude value of the device."""
        return self._latitude

    @property
    def longitude(self) -> float:
        """Return longitude value of the device."""
        return self._longitude

    @property
    def location_name(self) -> str:
        """Return a location name for the entity."""
        return self._location_name

    @property
    def location_accuracy(self) -> int:
        """Return the location accuracy of the device."""
        return self._location_accuracy

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return self._api_key

    async def _get_state_change(
        self, event: Event[EventStateChangedData], *args, **kwargs
    ):
        """Handle the state change."""
        if "test_button" in event.data["new_state"].attributes["friendly_name"]:
            self._latitude = random.uniform(-90, 90)
            self._longitude = random.uniform(-180, 180)
            self._location_name = "Test"
            self._location_accuracy = 1
            self.async_write_ha_state()
        else:
            _LOGGER.debug(
                "State change detected for %s, updating Dawarich", self._mobile_app
            )
            new_data = event.data["new_state"].attributes
            # We send the location to the Dawarich API
            response = await self._api.async_post_data(
                data={
                    "latitude": new_data["latitude"],
                    "longitude": new_data["longitude"],
                }
            )
            if response.success:
                _LOGGER.debug("Location sent to Dawarich API")
            else:
                _LOGGER.error(
                    "Failed to send location to Dawarich API, %s with context %s",
                    response.message,
                    response.context,
                )
