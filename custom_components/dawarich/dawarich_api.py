"""API class for Dawarich."""

from dataclasses import dataclass
import datetime
import aiohttp


@dataclass
class DawarichResponse:
    """Dawarich API response."""

    success: bool
    message: str
    context: str = ""


class DawarichAPI:
    # TODO: move to PyPI package
    def __init__(self, url: str, api_key: str, name: str):
        """Initialize the API."""
        self.url = url
        self.api_key = api_key
        self.name = name

    async def async_post_data(self, data: dict[str, str]) -> DawarichResponse:
        """Post data to the API."""
        json_data = {
            "locations": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            float(data["longitude"]),
                            float(data["latitude"]),
                        ],
                    },
                    "properties": {
                        "timestamp": data.get(
                            "timestamp", datetime.date.today().isoformat()
                        ),
                        "altitude": data.get("altitude", 0),
                        "speed": data.get("speed", 0),
                        "horizontal_accuracy": data.get("horizontal_accuracy", 0),
                        "vertical_accuracy": data.get("vertical_accuracy", 0),
                        "motion": [],
                        "pauses": False,
                        "activity": data.get("activity", "unknown"),
                        "desired_accuracy": 0,
                        "deffered": 0,
                        "significant_change": "unknown",
                        "locations_in_payload": 1,
                        "device_id": self.name,
                        "wifi": data.get("wifi", "unknown"),
                        "battery_state": data.get("battery_state", "unknown"),
                        "battery_level": data.get("battery_level", "unknown"),
                    },
                }
            ]
        }
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                self.url + f"/api/v1/overland/batches?api_key={self.api_key}",
                json=json_data,
            )
            if response.status == 201:
                return DawarichResponse(success=True, message="Data sent successfully")
            if response.status == 401:
                return DawarichResponse(success=False, message="Unauthorized")
            return DawarichResponse(
                success=False, message="Failed to send data", context=str(response.text)
            )
