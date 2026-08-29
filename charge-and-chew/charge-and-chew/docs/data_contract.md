# Data Contract: `backend` → `frontend`

To let both team members build in parallel, the backend exposes **one function** that returns a fully-formed JSON-serializable dict. The frontend should build against this shape from day one (using mock data if the real backend isn't ready yet).

## Entry point

```python
from backend.trip_planner import plan_trip

trip_plan = plan_trip(
    origin="Seattle, WA",
    destination="San Francisco, CA",
    vehicle_model="Tesla Model 3 Long Range",
    start_soc=90,          # percent, 0-100
    min_soc_buffer=15      # percent never to go below
)
```

## Return shape (`TripPlan`)

```jsonc
{
  "route": {
    "geometry": [[lat, lon], [lat, lon], "..."],   // full polyline for Folium
    "total_distance_km": 1310.4,
    "total_drive_time_min": 780
  },
  "vehicle": {
    "model": "Tesla Model 3 Long Range",
    "battery_kwh": 82,
    "consumption_kwh_per_km": 0.15
  },
  "charging_stops": [
    {
      "stop_number": 1,
      "location_name": "Centralia, WA",
      "lat": 46.716,
      "lon": -122.953,
      "charger_name": "Supercharger - Centralia",
      "connector_type": "CCS",
      "arrival_soc_percent": 22,
      "target_soc_percent": 80,
      "kwh_added": 47.6,
      "estimated_charge_time_min": 28,
      "cost_usd": 19.04,
      "dining_options": [
        {
          "name": "The Berry Fields Cafe",
          "cuisine": "American / Farm-to-table",
          "must_try_dish": "Marionberry pie",
          "walk_time_min": 4
        }
        // ... 2 more
      ]
    }
    // ... more stops
  ],
  "trip_summary": {
    "total_charging_cost_usd": 54.30,
    "total_charging_time_min": 65,
    "total_trip_time_min": 845,
    "num_charging_stops": 2,
    "num_dining_options": 6
  }
}
```

## Notes for the frontend

- `route.geometry` is a list of `[lat, lon]` pairs, ready to pass to `folium.PolyLine`.
- Each `charging_stops[i]` has its own `lat`/`lon` for a `folium.Marker`.
- `trip_summary` has everything needed for the metrics column — no extra computation needed on the frontend.

## Notes for the backend

- If Gemini or OpenChargeMap fails/rate-limits, `dining_options` or `charger_name` should degrade gracefully (empty list / `"Unknown"`) rather than raising — the frontend should never crash on a partial response.
- Keep `plan_trip()` synchronous and side-effect free (pure function of its inputs) so it's trivial to mock/test.
