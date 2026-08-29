"""
Orchestrates geocoding, routing, range planning, charger lookup, cost calc, and
dining recommendations into a single TripPlan dict — the contract with the frontend.
See docs/data_contract.md.
"""
from backend.geocoding import geocode
from backend.routing import get_route
from backend.range_engine import VehicleProfile, plan_waypoints
from backend.chargers import find_chargers_near
from backend.cost import kwh_needed, charging_cost_usd, estimate_charge_time_min
from backend.dining import get_dining_recommendations

# TODO: replace with a real vehicle spec lookup/table keyed by model name
VEHICLE_PROFILES = {
    "Tesla Model 3 Long Range": VehicleProfile("Tesla Model 3 Long Range", 82, 0.15),
    "Chevrolet Bolt EUV": VehicleProfile("Chevrolet Bolt EUV", 65, 0.17),
    "Hyundai Ioniq 5": VehicleProfile("Hyundai Ioniq 5", 77.4, 0.16),
}


def plan_trip(
    origin: str,
    destination: str,
    vehicle_model: str,
    start_soc: float,
    min_soc_buffer: float = 15,
) -> dict:
    vehicle = VEHICLE_PROFILES[vehicle_model]

    origin_coords = geocode(origin)
    dest_coords = geocode(destination)

    route = get_route(origin_coords, dest_coords)

    waypoint_distances_km = plan_waypoints(
        total_distance_km=route["distance_km"],
        vehicle=vehicle,
        start_soc_percent=start_soc,
        min_soc_buffer_percent=min_soc_buffer,
    )

    charging_stops = []
    for i, dist_km in enumerate(waypoint_distances_km, start=1):
        # NOTE: naive interpolation along straight-line geometry fraction —
        # fine for MVP; a proper implementation would walk the polyline by distance.
        fraction = dist_km / route["distance_km"]
        idx = min(int(fraction * len(route["geometry"])), len(route["geometry"]) - 1)
        lat, lon = route["geometry"][idx]

        nearby = find_chargers_near(lat, lon)
        charger = nearby[0] if nearby else {"name": "Unknown", "connector_types": []}

        kwh = kwh_needed(vehicle.battery_kwh, min_soc_buffer, 80)
        cost = charging_cost_usd(kwh)
        charge_time = estimate_charge_time_min(kwh)

        dining = get_dining_recommendations(
            location_name=charger["name"], lat=lat, lon=lon, charge_minutes=int(charge_time)
        )

        charging_stops.append({
            "stop_number": i,
            "location_name": charger["name"],
            "lat": lat,
            "lon": lon,
            "charger_name": charger["name"],
            "connector_type": charger["connector_types"][0] if charger["connector_types"] else "Unknown",
            "arrival_soc_percent": min_soc_buffer,
            "target_soc_percent": 80,
            "kwh_added": round(kwh, 1),
            "estimated_charge_time_min": charge_time,
            "cost_usd": cost,
            "dining_options": dining,
        })

    total_cost = sum(s["cost_usd"] for s in charging_stops)
    total_charge_time = sum(s["estimated_charge_time_min"] for s in charging_stops)

    return {
        "route": {
            "geometry": route["geometry"],
            "total_distance_km": round(route["distance_km"], 1),
            "total_drive_time_min": round(route["duration_min"], 1),
        },
        "vehicle": {
            "model": vehicle.model,
            "battery_kwh": vehicle.battery_kwh,
            "consumption_kwh_per_km": vehicle.consumption_kwh_per_km,
        },
        "charging_stops": charging_stops,
        "trip_summary": {
            "total_charging_cost_usd": round(total_cost, 2),
            "total_charging_time_min": round(total_charge_time, 1),
            "total_trip_time_min": round(route["duration_min"] + total_charge_time, 1),
            "num_charging_stops": len(charging_stops),
            "num_dining_options": sum(len(s["dining_options"]) for s in charging_stops),
        },
    }
