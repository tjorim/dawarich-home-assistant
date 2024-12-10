"""Config flow for Dawarich integration."""

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector

from . import DOMAIN


class DawarichConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Dawarich."""

    VERSION = 1

    def _get_form(self):
        data_schema = {
            vol.Required("friendly_name", default="Dawarich"): str,
            vol.Optional("mobile_app", msg="If you want to track your device"): selector.EntitySelector(
                selector.EntitySelectorConfig(device_class=["mobile_app"])
            ),
            vol.Required("url"): str,
            vol.Required("api_key"): str,
        }
        return self.async_show_form(step_id="user", data_schema=vol.Schema(data_schema))

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(
                title=user_input["friendly_name"], data=user_input
            )
        data_schema = {
            vol.Required("friendly_name", default="Dawarich"): str,
            vol.Optional("mobile_app", msg="If you want to track your device"): selector.EntitySelector(
                selector.EntitySelectorConfig(device_class=["mobile_app"])
            ),
            vol.Required("url"): str,
            vol.Required("api_key"): str,
        }
        return self.async_show_form(step_id="user", data_schema=vol.Schema(data_schema))
    
    async def async_step_reauth(self, data: dict[str, Any]) -> dict[str, Any]:
        """Handle re-authentication."""
        return self.async_show_form(step_id="user",data_schema=self._get_form())
