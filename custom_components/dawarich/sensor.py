"""Show statistical data from your Dawarich instance."""

import logging
from datetime import timedelta
from typing import TYPE_CHECKING, Any

from dawarich_api import DawarichAPI
from dawarich_api.api_calls import StatsResponseModel
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.const import UnitOfLength
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

if TYPE_CHECKING:
    from .config_flow import DawarichConfigFlow

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES = (
    SensorEntityDescription(
        key="total_distance_km", native_unit_of_measurement=UnitOfLength.KILOMETERS, name="Total Distance"
    ),
    SensorEntityDescription(
        key="total_points_tracked", native_unit_of_measurement="points", name="Total Points Tracked"
    ),
    SensorEntityDescription(
        key="total_reverse_geocoded_points", native_unit_of_measurement="points", name="Total Reverse Geocoded Points"
    ),
    SensorEntityDescription(
        key="total_countries_visited", native_unit_of_measurement="countries", name="Total Countries Visited"
    ),
    SensorEntityDescription(
        key="total_cities_visited", native_unit_of_measurement="cities", name="Total Cities Visited"
    ),
)
UPDATE_INTERVAL = timedelta(seconds=20)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: "DawarichConfigFlow",
    async_add_entities: AddEntitiesCallback,
):
    """Set up Dawarich sensor."""
    api_key = entry.data["api_key"]
    url = entry.data["url"]
    api = DawarichAPI(url=url, api_key=api_key)
    coordinator = DawarichCoordinator(hass, api)
    await coordinator.async_config_entry_first_refresh()
    sensors = [
        DawarichSensor(url, api_key, entry.data["friendly_name"], desc, coordinator)
        for desc in SENSOR_TYPES
    ]
    async_add_entities(sensors)


class DawarichCoordinator(DataUpdateCoordinator):
    """Custom coordinator."""

    def __init__(self, hass: HomeAssistant, api: DawarichAPI):
        """Initialize coordinator."""
        super().__init__(
            hass, _LOGGER, name="Dawarich Sensor", update_interval=UPDATE_INTERVAL
        )
        self.api = api

    async def _async_update_data(self) -> dict[str, Any]:
        response = await self.api.get_stats()
        match response.response_code:
            case 200:
                return response.response.dict() # type: ignore
            case 401:
                _LOGGER.error("Invalid credentials when trying to fetch stats from Dawarich")
                raise ConfigEntryAuthFailed("Invalid API key")
            case _:
                _LOGGER.error("Error fetching data from Dawarich (status %s) %s", response.response_code, response.error)
                raise UpdateFailed from Warning(f"Error fetching data from Dawarich (status {response.response_code})")


class DawarichSensor(CoordinatorEntity, SensorEntity): # type: ignore
    """Representation fo a Dawarich sensor."""

    def __init__(
        self,
        url: str,
        api_key: str,
        friendly_name: str,
        description: SensorEntityDescription,
        coordinator: DawarichCoordinator,
    ):
        """Initialize Dawarich sensor."""
        super().__init__(coordinator)
        self._api_key = api_key
        self._url = url
        self._api = DawarichAPI(url=url, api_key=api_key)
        self._friendly_name = friendly_name
        self.entity_description = description
        self._attr_unique_id = api_key + "/" + description.key

    @property
    def native_value(self) -> StateType: # type: ignore
        """Return the state of the device."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data[self.entity_description.key]
    
    @property
    def name(self) -> str: # type: ignore
        """Return the name of the sensor."""
        if isinstance(self.entity_description.name, str):
            return f"{self._friendly_name} {self.entity_description.name.title()}"
        _LOGGER.error("Name is not a string for %s", self.entity_description.key)
        return f"{self._friendly_name}"
