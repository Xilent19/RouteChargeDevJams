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

def soc_after_distance(
    vehicle: VehicleProfile,
    start_soc_percent: float,
    distance_km: float,
) -> float:
    """
    Calculate the battery SOC remaining after driving a given distance.
    """

    energy_used_kwh = distance_km * vehicle.consumption_kwh_per_km

    soc_used_percent = (
        energy_used_kwh / vehicle.battery_kwh
    ) * 100

    remaining_soc = start_soc_percent - soc_used_percent

    return max(0, round(remaining_soc, 1))

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


def calculate_leg_soc(
    vehicle: VehicleProfile,
    start_soc_percent: float,
    distance_km: float,
    min_soc_buffer_percent: float,
) -> dict:
    """
    Calculate battery SOC before and after a driving leg.

    Returns whether the vehicle stays above the required
    minimum SOC buffer.
    """

    arrival_soc = soc_after_distance(
        vehicle=vehicle,
        start_soc_percent=start_soc_percent,
        distance_km=distance_km,
    )

    return {
        "start_soc_percent": start_soc_percent,
        "distance_km": distance_km,
        "arrival_soc_percent": arrival_soc,
        "buffer_percent": min_soc_buffer_percent,
        "safe": arrival_soc >= min_soc_buffer_percent,
    }


def plan_charging_legs(
    total_distance_km: float,
    vehicle: VehicleProfile,
    start_soc_percent: float,
    min_soc_buffer_percent: float,
    target_soc_percent: float = 80,
) -> list[dict]:
    """
    Create charging legs with estimated arrival SOC.

    Each charging leg contains the distance from the origin,
    estimated SOC on arrival, and target SOC after charging.
    """

    waypoint_distances = plan_waypoints(
        total_distance_km=total_distance_km,
        vehicle=vehicle,
        start_soc_percent=start_soc_percent,
        min_soc_buffer_percent=min_soc_buffer_percent,
        target_soc_percent=target_soc_percent,
    )

    legs = []

    previous_distance = 0.0
    current_soc = start_soc_percent

    for stop_number, waypoint_distance in enumerate(waypoint_distances, start=1):
        leg_distance = waypoint_distance - previous_distance

        arrival_soc = soc_after_distance(
            vehicle=vehicle,
            start_soc_percent=current_soc,
            distance_km=leg_distance,
        )

        legs.append({
            "stop_number": stop_number,
            "distance_from_origin_km": round(waypoint_distance, 1),
            "leg_distance_km": round(leg_distance, 1),
            "arrival_soc_percent": arrival_soc,
            "target_soc_percent": target_soc_percent,
        })

        current_soc = target_soc_percent
        previous_distance = waypoint_distance

    return legs


def check_charger_reachability(
    vehicle: VehicleProfile,
    start_soc_percent: float,
    distance_km: float,
    min_soc_buffer_percent: float,
) -> dict:
    """
    Check whether a charger can be safely reached and
    report the estimated SOC on arrival.
    """

    arrival_soc = soc_after_distance(
        vehicle=vehicle,
        start_soc_percent=start_soc_percent,
        distance_km=distance_km,
    )

    return {
        "distance_km": round(distance_km, 1),
        "arrival_soc_percent": arrival_soc,
        "min_soc_buffer_percent": min_soc_buffer_percent,
        "reachable": arrival_soc >= min_soc_buffer_percent,
    }


if __name__ == "__main__":
    vehicle = VehicleProfile(
        model="Typical EV",
        battery_kwh=60,
        consumption_kwh_per_km=0.1667,
    )

    print(check_charger_reachability(vehicle, 80, 228, 15))
    print(check_charger_reachability(vehicle, 80, 241, 15))