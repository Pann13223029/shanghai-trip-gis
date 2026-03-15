#!/usr/bin/env python3
"""
Shanghai Trip CO2 Transport Calculator

Reads route GeoJSON files and computes per-segment, per-day,
and trip-total CO2 emissions using Shanghai-specific emission factors.

Usage:
    python3 tools/co2-calculator.py

Output:
    Prints a formatted report to stdout.
    Optionally writes results to data/analysis/co2-summary.json

Sources:
    See docs/sustainability-methodology.md for emission factor sources.
"""

import json
import os
from pathlib import Path

# ============================================================
# SHANGHAI-SPECIFIC EMISSION FACTORS (g CO2 per person per km)
# ============================================================
EMISSION_FACTORS = {
    "walking":  0,
    "cycling":  0,
    "metro":    29,     # Shanghai Shentong Metro Group, 2024
    "bus":      65,     # Shanghai Bus Company, 30% electric fleet
    "taxi":     120,    # Petrol taxi, avg 1.5 passengers
    "e-taxi":   45,     # EV ride-hail, Shanghai grid factor
    "train":    6,      # HSR, China State Railway Group
    "maglev":   95,     # Shanghai Maglev, NDRC data
}

# Contextual comparisons
CONTEXT = {
    "shanghai_commuter_daily_g":  580,   # 20km round trip by metro
    "flight_bkk_sha_one_way_kg":  250,  # Bangkok-Shanghai estimate
}


def load_route_file(filepath):
    """Load a GeoJSON route file and return its features."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("features", [])


def compute_segment_co2(segment):
    """Compute CO2 for a single route segment."""
    props = segment.get("properties", {})
    mode = props.get("mode", "walking")
    distance_km = props.get("distance_km", 0)

    factor = EMISSION_FACTORS.get(mode, 0)
    co2_g = distance_km * factor

    return {
        "from": props.get("from_name", "?"),
        "to": props.get("to_name", "?"),
        "mode": mode,
        "distance_km": distance_km,
        "duration_min": props.get("duration_min", 0),
        "co2_g": round(co2_g, 1),
        "emission_factor": factor,
    }


def compute_day(day_num, features):
    """Compute CO2 for all segments in a day."""
    segments = []
    total_co2 = 0
    total_distance = 0
    mode_breakdown = {}

    for feature in features:
        result = compute_segment_co2(feature)
        segments.append(result)
        total_co2 += result["co2_g"]
        total_distance += result["distance_km"]

        mode = result["mode"]
        if mode not in mode_breakdown:
            mode_breakdown[mode] = {"distance_km": 0, "co2_g": 0, "segments": 0}
        mode_breakdown[mode]["distance_km"] += result["distance_km"]
        mode_breakdown[mode]["co2_g"] += result["co2_g"]
        mode_breakdown[mode]["segments"] += 1

    # Compute all-taxi alternative
    all_taxi_co2 = total_distance * EMISSION_FACTORS["taxi"]

    return {
        "day": day_num,
        "segments": segments,
        "total_co2_g": round(total_co2, 1),
        "total_distance_km": round(total_distance, 1),
        "mode_breakdown": mode_breakdown,
        "all_taxi_co2_g": round(all_taxi_co2, 1),
        "co2_saved_vs_taxi_g": round(all_taxi_co2 - total_co2, 1),
        "co2_saved_vs_taxi_pct": round((1 - total_co2 / all_taxi_co2) * 100, 1) if all_taxi_co2 > 0 else 0,
    }


def print_report(days, trip_total):
    """Print a formatted CO2 report."""
    print("=" * 65)
    print("  SHANGHAI TRIP — TRANSPORT CO2 REPORT")
    print("  Emission factors: Shanghai-specific (see methodology doc)")
    print("=" * 65)

    for day in days:
        print(f"\n  DAY {day['day']}")
        print(f"  {'─' * 60}")

        for seg in day["segments"]:
            mode_str = f"[{seg['mode']}]".ljust(10)
            co2_str = f"{seg['co2_g']:>7.0f}g"
            dist_str = f"{seg['distance_km']:.1f}km"
            print(f"    {seg['from'][:20]:<20} → {seg['to'][:20]:<20}")
            print(f"      {mode_str} {dist_str:>8}  {seg['duration_min']:>3}min  {co2_str}")

        print(f"\n    {'─' * 55}")
        print(f"    Total:  {day['total_distance_km']:.1f} km  |  {day['total_co2_g']:.0f}g CO2")
        print(f"    If all taxi: {day['all_taxi_co2_g']:.0f}g  |  Saved: {day['co2_saved_vs_taxi_g']:.0f}g ({day['co2_saved_vs_taxi_pct']:.0f}%)")

        print(f"\n    Mode breakdown:")
        for mode, data in sorted(day["mode_breakdown"].items()):
            pct = (data["distance_km"] / day["total_distance_km"] * 100) if day["total_distance_km"] > 0 else 0
            bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
            print(f"      {mode:<10} {bar} {pct:>5.1f}%  ({data['distance_km']:.1f}km, {data['co2_g']:.0f}g)")

    # Trip summary
    print(f"\n{'=' * 65}")
    print(f"  TRIP SUMMARY")
    print(f"  {'─' * 60}")
    print(f"    Total distance:     {trip_total['total_distance_km']:.1f} km")
    print(f"    Total CO2:          {trip_total['total_co2_g']:.0f}g  ({trip_total['total_co2_kg']:.2f} kg)")
    print(f"    If all taxi:        {trip_total['all_taxi_co2_g']:.0f}g  ({trip_total['all_taxi_co2_kg']:.2f} kg)")
    print(f"    CO2 saved:          {trip_total['co2_saved_g']:.0f}g  ({trip_total['co2_saved_pct']:.0f}%)")
    print(f"    Avg daily CO2:      {trip_total['avg_daily_co2_g']:.0f}g")

    print(f"\n  CONTEXT COMPARISON")
    print(f"  {'─' * 60}")
    commuter = CONTEXT["shanghai_commuter_daily_g"]
    flight = CONTEXT["flight_bkk_sha_one_way_kg"] * 1000
    print(f"    Shanghai commuter (daily metro):  {commuter:>6}g")
    print(f"    Your avg daily transport:         {trip_total['avg_daily_co2_g']:>6.0f}g")
    ratio = trip_total["avg_daily_co2_g"] / commuter if commuter > 0 else 0
    print(f"    Ratio: {ratio:.1f}x a local commuter's daily transport")
    print(f"")
    print(f"    International flight (one way):   {flight:>6.0f}g  ({CONTEXT['flight_bkk_sha_one_way_kg']} kg)")
    print(f"    Your entire trip ground transport: {trip_total['total_co2_g']:>6.0f}g  ({trip_total['total_co2_kg']:.2f} kg)")
    if trip_total["total_co2_g"] > 0:
        flight_ratio = flight / trip_total["total_co2_g"]
        print(f"    One flight = {flight_ratio:.0f}x your entire trip's ground transport")
    print(f"\n{'=' * 65}")


def main():
    project_root = Path(__file__).parent.parent
    routes_dir = project_root / "data" / "routes"
    output_dir = project_root / "data" / "analysis"

    days = []
    trip_distance = 0
    trip_co2 = 0
    trip_taxi_co2 = 0

    for day_num in range(1, 7):
        filepath = routes_dir / f"day-{day_num}.geojson"
        if not filepath.exists():
            continue

        features = load_route_file(filepath)
        if not features:
            continue

        day_result = compute_day(day_num, features)
        days.append(day_result)
        trip_distance += day_result["total_distance_km"]
        trip_co2 += day_result["total_co2_g"]
        trip_taxi_co2 += day_result["all_taxi_co2_g"]

    num_days = len(days) if days else 1
    trip_total = {
        "total_distance_km": round(trip_distance, 1),
        "total_co2_g": round(trip_co2, 1),
        "total_co2_kg": round(trip_co2 / 1000, 2),
        "all_taxi_co2_g": round(trip_taxi_co2, 1),
        "all_taxi_co2_kg": round(trip_taxi_co2 / 1000, 2),
        "co2_saved_g": round(trip_taxi_co2 - trip_co2, 1),
        "co2_saved_pct": round((1 - trip_co2 / trip_taxi_co2) * 100, 1) if trip_taxi_co2 > 0 else 0,
        "avg_daily_co2_g": round(trip_co2 / num_days, 1),
        "days_computed": num_days,
    }

    print_report(days, trip_total)

    # Save JSON output
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "co2-summary.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"days": days, "trip_total": trip_total, "emission_factors": EMISSION_FACTORS, "context": CONTEXT}, f, indent=2, ensure_ascii=False)
    print(f"\n  Results saved to: {output_path.relative_to(project_root)}")


if __name__ == "__main__":
    main()
