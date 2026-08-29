"""
Smart Range & Buffer Engine.

Given a route's total distance and a vehicle's battery specs, determine how many
charging stops are required, and roughly where along the route (as a fraction of
total distance) each stop should be — respecting a minimum SOC buffer so the
battery is never driven to empty.
"""
from dataclasses import dataclass


@dataclass
class VehicleProfile:
    model: str
    battery_kwh: float
    consumption_kwh_per_km: float


def max_range_km(vehicle: VehicleProfile, usable_soc_percent: float) -> float:
    """Max distance (km) drivable on a given usable SOC window."""
    usable_kwh = vehicle.battery_kwh * (usable_soc_percent / 100)
    return usable_kwh / vehicle.consumption_kwh_per_km


def plan_waypoints(
    total_distance_km: float,
    vehicle: VehicleProfile,
    start_soc_percent: float,
    min_soc_buffer_percent: float,
    target_soc_percent: float = 80,
) -> list[float]:
    """
    Returns a list of distances (km from origin) at which a charging stop is needed,
    assuming the driver charges back up to `target_soc_percent` each time.

    This is intentionally simple (flat consumption rate, no elevation/weather
    modeling) — good enough for a hackathon MVP, documented as a future improvement.
    """
    usable_start = start_soc_percent - min_soc_buffer_percent
    leg_range = max_range_km(vehicle, target_soc_percent - min_soc_buffer_percent)

    stops = []
    distance_covered = max_range_km(vehicle, usable_start)

    while distance_covered < total_distance_km:
        stops.append(round(distance_covered, 1))
        distance_covered += leg_range

    return stops
