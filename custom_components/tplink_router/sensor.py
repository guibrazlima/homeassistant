from dataclasses import dataclass
from collections.abc import Callable
from typing import Any
from homeassistant.components.sensor import (
    SensorStateClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.const import PERCENTAGE, SIGNAL_STRENGTH_DECIBELS_MILLIWATT, UnitOfDataRate, UnitOfInformation
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from .const import DOMAIN
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC, DeviceInfo
from .coordinator import TPLinkRouterCoordinator
from tplinkrouterc6u import Status, LTEStatus


@dataclass
class TPLinkRouterSensorRequiredKeysMixin:
    value: Callable[[Status], Any]


@dataclass
class TPLinkRouterLTESensorRequiredKeysMixin:
    value: Callable[[LTEStatus], Any]


@dataclass
class TPLinkRouterSensorEntityDescription(
    SensorEntityDescription, TPLinkRouterSensorRequiredKeysMixin
):
    """A class that describes sensor entities."""

    sensor_type: str = "status"


@dataclass
class TPLinkRouterLTESensorEntityDescription(
    SensorEntityDescription, TPLinkRouterLTESensorRequiredKeysMixin
):
    """A class that describes LTEStatus entities."""

    sensor_type: str = "lte_status"


@dataclass
class TPLinkRouterMeshSensorEntityDescription(SensorEntityDescription):
    value: Callable[[TPLinkRouterCoordinator, dict], Any] | None = None
    sensor_type: str = "mesh"


SENSOR_TYPES: tuple[TPLinkRouterSensorEntityDescription, ...] = (
    TPLinkRouterSensorEntityDescription(
        key="guest_wifi_clients_total",
        name="Total guest wifi clients",
        icon="mdi:account-multiple",
        state_class=SensorStateClass.TOTAL,
        value=lambda status: status.guest_clients_total,
    ),
    TPLinkRouterSensorEntityDescription(
        key="wifi_clients_total",
        name="Total main wifi clients",
        icon="mdi:account-multiple",
        state_class=SensorStateClass.TOTAL,
        value=lambda status: status.wifi_clients_total,
    ),
    TPLinkRouterSensorEntityDescription(
        key="wired_clients_total",
        name="Total wired clients",
        icon="mdi:account-multiple",
        state_class=SensorStateClass.TOTAL,
        value=lambda status: status.wired_total,
    ),
    TPLinkRouterSensorEntityDescription(
        key="iot_clients_total",
        name="Total IoT clients",
        icon="mdi:account-multiple",
        state_class=SensorStateClass.TOTAL,
        value=lambda status: status.iot_clients_total,
    ),
    TPLinkRouterSensorEntityDescription(
        key="clients_total",
        name="Total clients",
        icon="mdi:account-multiple",
        state_class=SensorStateClass.TOTAL,
        value=lambda status: status.clients_total,
    ),
    TPLinkRouterSensorEntityDescription(
        key="cpu_used",
        name="CPU used",
        icon="mdi:cpu-64-bit",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        suggested_display_precision=1,
        value=lambda status: (status.cpu_usage * 100) if status.cpu_usage is not None else None,
    ),
    TPLinkRouterSensorEntityDescription(
        key="memory_used",
        name="Memory used",
        icon="mdi:memory",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        suggested_display_precision=1,
        value=lambda status: (status.mem_usage * 100) if status.mem_usage is not None else None,
    ),
    TPLinkRouterSensorEntityDescription(
        key="conn_type",
        name="Connection Type",
        icon="mdi:wan",
        value=lambda status: status.conn_type,
    ),
    TPLinkRouterSensorEntityDescription(
        key="wan_ipv4_addr",
        name="WAN IPv4 Address",
        icon="mdi:wan",
        value=lambda status: status.wan_ipv4_addr,
    ),
    TPLinkRouterSensorEntityDescription(
        key="lan_ipv4_addr",
        name="LAN IPv4 Address",
        icon="mdi:lan",
        value=lambda status: status.lan_ipv4_addr,
    ),
)

LTE_SENSOR_TYPES: tuple[TPLinkRouterLTESensorEntityDescription, ...] = (
    TPLinkRouterLTESensorEntityDescription(
        key="lte_enabled",
        name="LTE Enabled",
        icon="mdi:sim-outline",
        value=lambda status: status.enable,
    ),
    TPLinkRouterLTESensorEntityDescription(
        key="lte_connect_status",
        name="LTE Connection Status",
        icon="mdi:sim-outline",
        value=lambda status: status.connect_status,
    ),
    TPLinkRouterLTESensorEntityDescription(
        key="lte_network_type",
        name="LTE Network Type",
        icon="mdi:sim-outline",
        value=lambda status: status.network_type,
    ),
    TPLinkRouterLTESensorEntityDescription(
        key="lte_network_type_info",
        name="LTE Network Type Info",
        icon="mdi:sim-outline",
        value=lambda status: status.network_type_info,
    ),
    TPLinkRouterLTESensorEntityDescription(
        key="lte_sim_status",
        name="LTE SIM Status",
        icon="mdi:sim-outline",
        value=lambda status: status.sim_status,
    ),
    TPLinkRouterLTESensorEntityDescription(
        key="lte_sim_status_info",
        name="LTE SIM Status Info",
        icon="mdi:sim-outline",
        value=lambda status: status.sim_status_info,
    ),
    TPLinkRouterLTESensorEntityDescription(
        key="lte_total_statistics",
        name="LTE Total Statistics",
        icon="mdi:sim-outline",
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement=UnitOfInformation.BYTES,
        value=lambda status: status.total_statistics,
    ),
    TPLinkRouterLTESensorEntityDescription(
        key="lte_cur_rx_speed",
        name="LTE Current RX Speed",
        icon="mdi:sim-outline",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfDataRate.BYTES_PER_SECOND,
        value=lambda status: status.cur_rx_speed,
    ),
    TPLinkRouterLTESensorEntityDescription(
        key="lte_cur_tx_speed",
        name="LTE Current TX Speed",
        icon="mdi:sim-outline",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfDataRate.BYTES_PER_SECOND,
        value=lambda status: status.cur_tx_speed,
    ),
    TPLinkRouterLTESensorEntityDescription(
        key="lte_sms_unread_count",
        name="Unread SMS",
        icon="mdi:sim-outline",
        state_class=SensorStateClass.TOTAL,
        value=lambda status: status.sms_unread_count,
    ),
    TPLinkRouterLTESensorEntityDescription(
        key="lte_sig_level",
        name="LTE Signal Level",
        icon="mdi:sim-outline",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        value=lambda status: status.sig_level * 25,
    ),
    TPLinkRouterLTESensorEntityDescription(
        key="lte_rsrp",
        name="LTE RSRP",
        icon="mdi:sim-outline",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        value=lambda status: status.rsrp,
    ),
    TPLinkRouterLTESensorEntityDescription(
        key="lte_rsrq",
        name="LTE RSRQ",
        icon="mdi:sim-outline",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        value=lambda status: status.rsrq,
    ),
    TPLinkRouterLTESensorEntityDescription(
        key="lte_snr",
        name="LTE SNR",
        icon="mdi:sim-outline",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        value=lambda status: 0.1 * status.snr,
    ),
    TPLinkRouterLTESensorEntityDescription(
        key="lte_isp_name",
        name="LTE ISP Name",
        icon="mdi:sim-outline",
        value=lambda status: status.isp_name,
    ),
)


def _safe_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


MESH_SENSOR_TYPES: tuple[TPLinkRouterMeshSensorEntityDescription, ...] = (
    TPLinkRouterMeshSensorEntityDescription(
        key="mesh_node_status",
        name="Status",
        icon="mdi:access-point-network",
        value=lambda coord, node: node.get("inet_status"),
    ),
    TPLinkRouterMeshSensorEntityDescription(
        key="mesh_node_backhaul_speed",
        name="Backhaul Speed",
        icon="mdi:lan",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
        value=lambda coord, node: _safe_int(node.get("backhual_speed")),
    ),
    TPLinkRouterMeshSensorEntityDescription(
        key="mesh_node_backhaul_max_speed",
        name="Backhaul Max Speed",
        icon="mdi:lan",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
        value=lambda coord, node: _safe_int(node.get("backhual_max_speed")),
    ),
    TPLinkRouterMeshSensorEntityDescription(
        key="mesh_node_clients_total",
        name="Connected Clients",
        icon="mdi:account-multiple",
        state_class=SensorStateClass.MEASUREMENT,
        value=lambda coord, node: coord.mesh_clients_by_node.get(node.get("mac")),
    ),
    TPLinkRouterMeshSensorEntityDescription(
        key="mesh_node_signal_2g",
        name="Signal 2.4 GHz",
        icon="mdi:wifi",
        state_class=SensorStateClass.MEASUREMENT,
        value=lambda coord, node: _safe_int(node.get("signal_level", {}).get("band2_4")),
    ),
    TPLinkRouterMeshSensorEntityDescription(
        key="mesh_node_signal_5g",
        name="Signal 5 GHz",
        icon="mdi:wifi",
        state_class=SensorStateClass.MEASUREMENT,
        value=lambda coord, node: _safe_int(node.get("signal_level", {}).get("band5")),
    ),
    TPLinkRouterMeshSensorEntityDescription(
        key="mesh_node_signal_6g",
        name="Signal 6 GHz",
        icon="mdi:wifi",
        state_class=SensorStateClass.MEASUREMENT,
        value=lambda coord, node: _safe_int(node.get("signal_level", {}).get("band6")),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    # Ensure mesh data is available before creating mesh entities.
    if hasattr(coordinator, "_update_mesh"):
        try:
            await coordinator._update_mesh()
        except Exception:
            pass

    sensors = []

    for description in SENSOR_TYPES:
        sensors.append(TPLinkRouterSensor(coordinator, description))

    if coordinator.lte_status is not None:
        for description in LTE_SENSOR_TYPES:
            sensors.append(TPLinkRouterSensor(coordinator, description))

    async_add_entities(sensors, False)

    mesh_added: set[str] = set()

    @callback
    def _add_mesh_entities() -> None:
        new_entities = []
        for node in coordinator.mesh_nodes:
            mac = node.get("mac")
            if not mac or mac in mesh_added:
                continue
            for description in MESH_SENSOR_TYPES:
                new_entities.append(TPLinkRouterMeshSensor(coordinator, node, description))
            mesh_added.add(mac)
        if new_entities:
            async_add_entities(new_entities, False)

    _add_mesh_entities()
    coordinator.async_add_listener(_add_mesh_entities)


class TPLinkRouterSensor(
    CoordinatorEntity[TPLinkRouterCoordinator], SensorEntity
):
    _attr_has_entity_name = True
    entity_description: TPLinkRouterSensorEntityDescription | TPLinkRouterLTESensorEntityDescription

    def __init__(
            self,
            coordinator: TPLinkRouterCoordinator,
            description: TPLinkRouterSensorEntityDescription | TPLinkRouterLTESensorEntityDescription,
    ) -> None:
        super().__init__(coordinator)

        self._attr_device_info = coordinator.device_info
        self._attr_unique_id = f"{coordinator.unique_id}_{DOMAIN}_{description.key}"
        self.entity_description = description

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        coordinator_data = getattr(self.coordinator, self.entity_description.sensor_type)
        self._attr_native_value = self.entity_description.value(coordinator_data)
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        coordinator_data = getattr(self.coordinator, self.entity_description.sensor_type)
        return self.entity_description.value(coordinator_data) is not None


class TPLinkRouterMeshSensor(CoordinatorEntity[TPLinkRouterCoordinator], SensorEntity):
    _attr_has_entity_name = True
    entity_description: TPLinkRouterMeshSensorEntityDescription

    def __init__(
            self,
            coordinator: TPLinkRouterCoordinator,
            node: dict,
            description: TPLinkRouterMeshSensorEntityDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._node = node
        self._node_mac = node.get("mac")
        self._node_name = node.get("nickname") or self._node_mac or "Mesh node"
        self._attr_unique_id = f"{coordinator.unique_id}_{DOMAIN}_mesh_{self._node_mac}_{description.key}"
        self._attr_name = description.name
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"mesh_{self._node_mac}")},
            connections={(CONNECTION_NETWORK_MAC, self._node_mac)},
            manufacturer="TPLink",
            model=node.get("device_model"),
            name=self._node_name,
            sw_version=node.get("software_ver"),
            hw_version=node.get("hardware_ver"),
            via_device=(DOMAIN, coordinator.status.lan_macaddr),
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        # Refresh node data from latest coordinator snapshot.
        node = next((n for n in self.coordinator.mesh_nodes if n.get("mac") == self._node_mac), self._node)
        self._node = node
        self._attr_native_value = self.entity_description.value(self.coordinator, node)
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        return self._node_mac is not None
