"""Select platform for Tessie integration."""

from __future__ import annotations

from tessie_api import set_seat_heat

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import TessieConfigEntry
from .const import TessieSeatHeaterOptions
from .entity import TessieEntity

SEAT_HEATERS = {
    "climate_state_seat_heater_left": "front_left",
    "climate_state_seat_heater_right": "front_right",
    "climate_state_seat_heater_rear_left": "rear_left",
    "climate_state_seat_heater_rear_center": "rear_center",
    "climate_state_seat_heater_rear_right": "rear_right",
    "climate_state_seat_heater_third_row_left": "third_row_left",
    "climate_state_seat_heater_third_row_right": "third_row_right",
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: TessieConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Tessie select platform from a config entry."""
    data = entry.runtime_data

    async_add_entities(
        TessieSeatHeaterSelectEntity(vehicle, key)
        for vehicle in data.vehicles
        for key in SEAT_HEATERS
        if key
        in vehicle.data_coordinator.data  # not all vehicles have rear center or third row
    )


class TessieSeatHeaterSelectEntity(TessieEntity, SelectEntity):
    """Select entity for current charge."""

    _attr_options = [
        TessieSeatHeaterOptions.OFF,
        TessieSeatHeaterOptions.LOW,
        TessieSeatHeaterOptions.MEDIUM,
        TessieSeatHeaterOptions.HIGH,
    ]

    @property
    def current_option(self) -> str | None:
        """Return the current selected option."""
        return self._attr_options[self._value]

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        level = self._attr_options.index(option)
        await self.run(set_seat_heat, seat=SEAT_HEATERS[self.key], level=level)
        self.set((self.key, level))
