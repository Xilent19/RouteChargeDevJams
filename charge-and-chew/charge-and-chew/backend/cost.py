"""
Charging cost calculations.
"""

# Rough regional average — replace with real per-station pricing where OCM provides it.
DEFAULT_COST_PER_KWH_USD = 0.42


def kwh_needed(battery_kwh: float, from_soc_percent: float, to_soc_percent: float) -> float:
    return battery_kwh * (to_soc_percent - from_soc_percent) / 100


def charging_cost_usd(kwh: float, cost_per_kwh: float = DEFAULT_COST_PER_KWH_USD) -> float:
    return round(kwh * cost_per_kwh, 2)


def estimate_charge_time_min(kwh: float, charger_kw: float = 150) -> float:
    """Rough estimate; real charging curves taper as SOC rises — good enough for MVP."""
    return round((kwh / charger_kw) * 60, 1)
