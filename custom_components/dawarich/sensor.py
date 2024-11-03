"""Show statistical data from your Dawarich instance."""

from dawarich_api import DawarichAPI
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.const import UnitOfLength
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from custom_components.dawarich.config_flow import DawarichConfigFlow

SENSOR_TYPES = SensorEntityDescription(
    key="total_distance", native_unit_of_measurement=UnitOfLength.KILOMETERS
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: DawarichConfigFlow,
    async_add_entities: AddEntitiesCallback,
):
    """Set up Dawarich sensor."""
    sensors = [DawarichSensor(entry["url"], entry["api_key"], entry["friendly_name"])]
    async_add_entities(sensors)


class DawarichSensor(SensorEntity):
    """Representation fo a Dawarich sensor."""

    def __init__(self, url: str, api_key: str, friendly_name: str):
        """Initialize Dawarich sensor."""
        self._api_key = api_key
        self._url = url
        self._api = DawarichAPI(url=url, api_key=api_key)
        self._friendly_name = friendly_name
        self._total_km = 199

    @property
    def native_value(self) -> StateType:
        """Return the state of the device."""
        return self._total_km
