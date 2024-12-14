"""Dawarich integration."""

from logging import getLogger

from dawarich_api import DawarichAPI
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, CONF_HOST, CONF_NAME
from homeassistant.core import Event, EventStateChangedData, HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.typing import ConfigType

from .const import CONF_DEVICE

_LOGGER = getLogger(__name__)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info=None,
) -> None:
    """Set up the sensor platform."""
    if not config.get(CONF_DEVICE):
        _LOGGER.info(
            "No mobile_app entity found in platform setup, skipping Dawarich mobile tracking setup"
        )
        return
    async_add_entities([DawarichDeviceTracker(entry=config, hass=hass)])


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    if not config_entry.data.get(CONF_DEVICE):
        _LOGGER.info(
            "No mobile_app entity found, skipping Dawarich mobile tracking setup"
        )
        return
    async_add_entities([DawarichDeviceTracker(entry=config_entry.data, hass=hass)])


class DawarichDeviceTracker(TrackerEntity):
    """Dawarich Sensor Class."""

    def __init__(self, entry: ConfigType, hass: HomeAssistant) -> None:
        """Initialize the sensor."""
        self._friendly_name = entry[CONF_NAME]
        self._url = entry[CONF_HOST]
        self._api_key = entry[CONF_API_KEY]
        self._mobile_app = entry[CONF_DEVICE]

        self._latitude = 0.0
        self._longitude = 0.0
        self._location_name = "Home"
        self._location_accuracy = 2

        self._api = entry.runtime_data.api

        self._hass = hass
        self._async_unsubscribe_state_changed = async_track_state_change_event(
            hass=self._hass,
            entity_ids=[self._mobile_app],
            action=self._get_state_change,
        )
        _LOGGER.debug("Dawarich Sensor initialized")

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

    async def _get_state_change(
        self, event: Event[EventStateChangedData], *args, **kwargs
    ):
        """Handle the state change."""
        _LOGGER.debug(
            "State change detected for %s, updating Dawarich", self._mobile_app
        )
        new_data = event.data["new_state"].attributes
        # We send the location to the Dawarich API
        response = await self._api.add_one_point(
            latitude=new_data["latitude"],
            longitude=new_data["longitude"],
            name=self._friendly_name,
        )
        if response.success:
            _LOGGER.debug("Location sent to Dawarich API")
        else:
            _LOGGER.error(
                "Error sending location to Dawarich API response code %s and error: %s",
                response.response_code,
                response.error,
            )
