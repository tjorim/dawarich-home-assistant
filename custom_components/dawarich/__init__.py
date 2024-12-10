"""The Dawarich integration."""

from dawarich_api import DawarichAPI
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed

from ..dawarich.sensor import DawarichCoordinator

DOMAIN = "dawarich"
VERSION = "0.2.1"

PLATFORMS: list[Platform] = [Platform.DEVICE_TRACKER, Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Dawarich from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Test and make sure the API key is valid 
    api_key = entry.data["api_key"]
    url = entry.data["url"]
    api = DawarichAPI(url=url, api_key=api_key)
    coordinator = DawarichCoordinator(hass, api)
    await coordinator.async_config_entry_first_refresh()

    # Setup the platforms if the API key is valid
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
