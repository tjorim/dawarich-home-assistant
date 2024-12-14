"""The Dawarich integration."""

from dataclasses import dataclass

from dawarich_api import DawarichAPI
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, CONF_HOST, CONF_NAME, CONF_SSL, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed

from .config_flow import DawarichConfigFlow
from .const import DOMAIN
from .coordinator import DawarichCoordinator
from .helpers import get_api

VERSION = "0.2.1"

PLATFORMS: list[Platform] = [Platform.DEVICE_TRACKER, Platform.SENSOR]

type DawarichConfigEntry = ConfigEntry[DawarichConfigEntryData]


@dataclass
class DawarichConfigEntryData:
    """Runtime data definitions."""

    api: DawarichAPI
    coordinator: DawarichCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: DawarichConfigEntry) -> bool:
    """Set up Dawarich from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    name = entry.data[CONF_NAME]
    host = entry.data[CONF_HOST]
    api_key = entry.data[CONF_API_KEY]
    use_ssl = entry.data[CONF_SSL]

    api = get_api(host, api_key, use_ssl)

    coordinator = DawarichCoordinator(hass, api)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = DawarichConfigEntryData(api=api, coordinator=coordinator)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
