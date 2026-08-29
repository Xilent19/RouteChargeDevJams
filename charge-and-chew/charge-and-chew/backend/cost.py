"""
Charging cost calculations.
"""

# Rough public fast-charging estimate for the MVP.
# Can be replaced with real per-station pricing later.
DEFAULT_COST_PER_KWH_INR = 18.0


def kwh_needed(
    battery_kwh: float,
    from_soc_percent: float,
    to_soc_percent: float,
) -> float:
    """Calculate energy needed to move from one SOC level to another."""
    return battery_kwh * (to_soc_percent - from_soc_percent) / 100


def charging_cost_inr(
    kwh: float,
    cost_per_kwh: float = DEFAULT_COST_PER_KWH_INR,
) -> float:
    """Calculate charging cost in Indian rupees."""
    return round(kwh * cost_per_kwh, 2)


def estimate_charge_time_min(
    kwh: float,
    charger_kw: float = 150,
) -> float:
    """
    Estimate charging time in minutes.

    Uses constant charging power for the MVP.
    Real EV charging curves taper at higher SOC.
    """
    return round((kwh / charger_kw) * 60, 1)

if __name__ == "__main__":
    energy = kwh_needed(60, 15, 80)

    print(f"Energy needed: {energy:.1f} kWh")
    print(f"Charging cost: ₹{charging_cost_inr(energy):.2f}")
    print(f"Charge time: {estimate_charge_time_min(energy):.1f} min")