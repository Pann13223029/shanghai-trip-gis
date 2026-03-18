#!/usr/bin/env python3
"""
Creates and populates a Google Sheet with the Shanghai trip itinerary.
Reads POI and route data from the project's GeoJSON files.

Usage:
    python3 tools/create-itinerary-sheet.py
"""

import json
import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================

PROJECT_ROOT = Path(__file__).parent.parent
SERVICE_ACCOUNT_FILE = PROJECT_ROOT / "service-account.json"
SHARE_WITH_EMAIL = "pann.phetra@gmail.com"  # Your personal Google account

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# Shanghai-specific emission factors (g CO2 per person per km)
EMISSION_FACTORS = {
    "walking": 0, "metro": 29, "taxi": 120,
    "bus": 65, "train": 6, "maglev": 95,
}

DAY_THEMES = {
    1: "Arrival & The Bund",
    2: "Old Town & French Concession",
    3: "Pudong Skyline",
    4: "Culture & Art",
    5: "Explore & Free Day",
    6: "Suzhou Day Trip",
}


# ============================================================
# DATA LOADING
# ============================================================

def load_pois():
    """Load all POIs from GeoJSON files, grouped by day."""
    poi_dir = PROJECT_ROOT / "data" / "poi"
    all_pois = []
    for f in sorted(poi_dir.glob("*.geojson")):
        with open(f, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            for feat in data.get("features", []):
                p = feat["properties"]
                coords = feat["geometry"]["coordinates"]
                p["_lng"] = coords[0]
                p["_lat"] = coords[1]
                p["_file"] = f.stem
                all_pois.append(p)
    return all_pois


def load_routes():
    """Load all routes from GeoJSON files."""
    routes_dir = PROJECT_ROOT / "data" / "routes"
    all_routes = {}
    for day in range(1, 7):
        f = routes_dir / f"day-{day}.geojson"
        if f.exists():
            with open(f, "r", encoding="utf-8") as fh:
                data = json.load(fh)
                routes = []
                for feat in data.get("features", []):
                    routes.append(feat["properties"])
                if routes:
                    all_routes[day] = routes
    return all_routes


def load_co2_summary():
    """Load precomputed CO2 data."""
    f = PROJECT_ROOT / "data" / "analysis" / "co2-summary.json"
    if f.exists():
        with open(f, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return None


# ============================================================
# SHEET CREATION
# ============================================================

EXISTING_SHEET_URL = "https://docs.google.com/spreadsheets/d/1ygvPoBHYxhrNQqCGjlNI6srOgTMV1-VkkNM43lVzkEg/edit"


def create_sheet(gc):
    """Open the existing Google Sheet."""
    sh = gc.open_by_url(EXISTING_SHEET_URL)
    print(f"Opened sheet: {sh.url}")
    return sh


def setup_overview_tab(sh, pois, routes, co2):
    """Create the Overview tab with trip summary."""
    ws = sh.sheet1
    ws.update_title("Overview")

    # Header
    rows = [
        ["SHANGHAI & SUZHOU TRIP ITINERARY 2026"],
        [""],
        ["TRIP SUMMARY"],
        ["Total days", 6],
        ["Shanghai days", 5],
        ["Suzhou day trip", 1],
        ["Total POIs", len(pois)],
        ["POIs with day assigned", len([p for p in pois if p.get("day")])],
        [""],
    ]

    # CO2 summary
    if co2:
        t = co2["trip_total"]
        rows.extend([
            ["TRANSPORT CO2 SUMMARY"],
            ["Total distance", f"{t['total_distance_km']} km"],
            ["Total CO2 (our plan)", f"{t['total_co2_kg']} kg"],
            ["Total CO2 (if all taxi)", f"{t['all_taxi_co2_kg']} kg"],
            ["CO2 saved", f"{t['co2_saved_pct']}%"],
            ["Avg daily CO2", f"{t['avg_daily_co2_g']}g"],
            [""],
        ])

    # Day themes
    rows.append(["DAY-BY-DAY OVERVIEW"])
    rows.append(["Day", "Theme", "POIs Planned", "Route Segments", "Est. CO2"])
    for day in range(1, 7):
        day_pois = [p for p in pois if p.get("day") == day]
        day_routes = routes.get(day, [])
        day_co2 = ""
        if co2:
            for d in co2.get("days", []):
                if d["day"] == day:
                    day_co2 = f"{d['total_co2_g']}g"
        rows.append([
            f"Day {day}",
            DAY_THEMES.get(day, ""),
            len(day_pois),
            len(day_routes),
            day_co2,
        ])

    rows.extend([
        [""],
        ["LINKS"],
        ["Live map", "https://pann13223029.github.io/shanghai-trip-gis/"],
        ["GitHub repo", "https://github.com/Pann13223029/shanghai-trip-gis"],
    ])

    ws.update(range_name="A1", values=rows)

    # Format header
    ws.format("A1", {"textFormat": {"bold": True, "fontSize": 16}})
    ws.format("A3", {"textFormat": {"bold": True, "fontSize": 12}})
    ws.format("A10", {"textFormat": {"bold": True, "fontSize": 12}})
    ws.format("A18", {"textFormat": {"bold": True, "fontSize": 12}})
    ws.format("A19:E19", {"textFormat": {"bold": True}, "backgroundColor": {"red": 0.9, "green": 0.95, "blue": 1.0}})
    ws.columns_auto_resize(0, 5)


def setup_day_tab(sh, day, pois, routes, co2_data):
    """Create a tab for a specific day."""
    theme = DAY_THEMES.get(day, "")
    tab_name = f"Day {day}"
    ws = sh.add_worksheet(title=tab_name, rows=100, cols=20)

    day_pois = sorted(
        [p for p in pois if p.get("day") == day],
        key=lambda p: p.get("id", "")
    )
    day_routes = routes.get(day, [])

    # Header
    rows = [
        [f"DAY {day} — {theme}"],
        [""],
    ]

    # Itinerary timeline
    rows.append(["TIME", "ACTIVITY", "LOCATION (EN)", "LOCATION (CN)", "TRANSPORT", "DISTANCE", "DURATION", "CO2", "COST (CNY)", "NOTES"])

    if day_routes:
        time_cursor = "09:00" if day != 1 else "14:00"
        if day == 6:
            time_cursor = "08:00"

        for i, route in enumerate(day_routes):
            mode = route.get("mode", "")
            dist = route.get("distance_km", 0)
            dur = route.get("duration_min", 0)
            co2_g = round(dist * EMISSION_FACTORS.get(mode, 0))

            # Add departure row
            rows.append([
                time_cursor,
                "Depart",
                route.get("from_name", ""),
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ])

            # Add transport row
            rows.append([
                "",
                f"→ {mode}",
                "",
                "",
                mode,
                f"{dist} km",
                f"{dur} min",
                f"{co2_g}g",
                "",
                "",
            ])

            # Calculate arrival time
            h, m = map(int, time_cursor.split(":"))
            m += dur
            h += m // 60
            m = m % 60
            time_cursor = f"{h:02d}:{m:02d}"

            # Add arrival row (last segment gets the destination)
            if i == len(day_routes) - 1:
                # Find POI details for destination
                dest_poi = next((p for p in day_pois if p.get("id") == route.get("to_id")), None)
                rows.append([
                    time_cursor,
                    "Arrive",
                    route.get("to_name", ""),
                    dest_poi.get("name_cn", "") if dest_poi else "",
                    "",
                    "",
                    "",
                    "",
                    dest_poi.get("est_cost_cny", "") if dest_poi else "",
                    "",
                ])

        # Add total row
        total_dist = sum(r.get("distance_km", 0) for r in day_routes)
        total_dur = sum(r.get("duration_min", 0) for r in day_routes)
        total_co2 = sum(
            round(r.get("distance_km", 0) * EMISSION_FACTORS.get(r.get("mode", ""), 0))
            for r in day_routes
        )
        rows.extend([
            [""],
            ["", "TOTALS", "", "", "", f"{total_dist:.1f} km", f"{total_dur} min", f"{total_co2}g", "", ""],
        ])

    # POI details section
    rows.extend([
        [""],
        [""],
        ["DAY'S POINTS OF INTEREST"],
        ["ID", "Name (EN)", "Name (CN)", "Category", "Priority", "Duration", "Cost (CNY)", "Hours", "Weather", "Sustainability Score", "Notes"],
    ])

    for p in day_pois:
        rows.append([
            p.get("id", ""),
            p.get("name_en", ""),
            p.get("name_cn", ""),
            p.get("category", ""),
            p.get("priority", ""),
            f"{p.get('est_duration_min', '')} min" if p.get("est_duration_min") else "",
            p.get("est_cost_cny", ""),
            p.get("opening_hours", ""),
            "Outdoor" if p.get("weather_sensitive") else "Indoor",
            p.get("sustainability_score", "N/A"),
            p.get("notes", "")[:100],  # Truncate long notes
        ])

    ws.update(range_name="A1", values=rows)

    # Format
    ws.format("A1", {"textFormat": {"bold": True, "fontSize": 14}})
    ws.format("A3:J3", {"textFormat": {"bold": True}, "backgroundColor": {"red": 0.85, "green": 0.92, "blue": 1.0}})

    # Find the POI header row
    poi_header_row = len(rows) - len(day_pois)
    ws.format(f"A{poi_header_row}:K{poi_header_row}", {
        "textFormat": {"bold": True},
        "backgroundColor": {"red": 0.9, "green": 0.95, "blue": 0.9}
    })

    ws.columns_auto_resize(0, 11)


def setup_all_pois_tab(sh, pois):
    """Create a tab listing all POIs."""
    ws = sh.add_worksheet(title="All POIs", rows=60, cols=20)

    rows = [
        ["ALL POINTS OF INTEREST"],
        [""],
        ["ID", "Name (EN)", "Name (CN)", "Category", "Day", "Priority",
         "Duration", "Cost", "Hours", "Sustainability", "Transit", "Heritage",
         "Community", "Walkability", "Env. Sensitivity", "Address"],
    ]

    sorted_pois = sorted(pois, key=lambda p: (p.get("day") or 99, p.get("category", ""), p.get("id", "")))

    for p in sorted_pois:
        rows.append([
            p.get("id", ""),
            p.get("name_en", ""),
            p.get("name_cn", ""),
            p.get("category", ""),
            p.get("day", ""),
            p.get("priority", ""),
            p.get("est_duration_min", ""),
            p.get("est_cost_cny", ""),
            p.get("opening_hours", ""),
            p.get("sustainability_score", ""),
            p.get("transit_access", ""),
            p.get("heritage_value", ""),
            p.get("community_impact", ""),
            p.get("walkability", ""),
            p.get("environmental_sensitivity", ""),
            p.get("address", ""),
        ])

    ws.update(range_name="A1", values=rows)
    ws.format("A1", {"textFormat": {"bold": True, "fontSize": 14}})
    ws.format("A3:P3", {"textFormat": {"bold": True}, "backgroundColor": {"red": 0.95, "green": 0.95, "blue": 0.95}})
    ws.columns_auto_resize(0, 16)


def setup_co2_tab(sh, co2):
    """Create a CO2 analysis tab."""
    if not co2:
        return

    ws = sh.add_worksheet(title="CO2 Analysis", rows=60, cols=10)

    rows = [
        ["TRANSPORT CO2 ANALYSIS"],
        ["Shanghai-specific emission factors (see sustainability-methodology.md)"],
        [""],
        ["EMISSION FACTORS"],
        ["Mode", "g CO2/km/person", "Source"],
        ["Walking", 0, "—"],
        ["Metro", 29, "Shanghai Shentong Metro Group 2024"],
        ["Bus", 65, "Shanghai Bus Company (30% EV fleet)"],
        ["Taxi (petrol)", 120, "Avg fuel economy, 1.5 passengers"],
        ["E-taxi (EV)", 45, "Shanghai grid factor × EV consumption"],
        ["HSR Train", 6, "China State Railway Group"],
        ["Maglev", 95, "NDRC rail energy data"],
        [""],
        ["DAILY BREAKDOWN"],
        ["Day", "Distance (km)", "CO2 (g)", "CO2 (kg)", "If All Taxi (g)", "Saved (%)", "Top Mode"],
    ]

    for d in co2.get("days", []):
        # Find the mode with most distance
        top_mode = ""
        top_dist = 0
        for mode, data in d.get("mode_breakdown", {}).items():
            if data["distance_km"] > top_dist:
                top_dist = data["distance_km"]
                top_mode = mode

        rows.append([
            f"Day {d['day']}",
            d["total_distance_km"],
            d["total_co2_g"],
            round(d["total_co2_g"] / 1000, 2),
            d["all_taxi_co2_g"],
            f"{d['co2_saved_vs_taxi_pct']}%",
            top_mode,
        ])

    t = co2["trip_total"]
    rows.extend([
        [""],
        ["TRIP TOTAL", t["total_distance_km"], t["total_co2_g"], t["total_co2_kg"],
         t["all_taxi_co2_g"], f"{t['co2_saved_pct']}%", ""],
        [""],
        ["CONTEXT"],
        ["Shanghai commuter daily (20km metro)", "", "580g", "", "", "", ""],
        ["Our avg daily", "", f"{t['avg_daily_co2_g']}g", "", "", "", ""],
        ["International flight (one way)", "", "250,000g", "250 kg", "", "", ""],
        ["Our entire trip ground transport", "", f"{t['total_co2_g']}g", f"{t['total_co2_kg']} kg", "", "", ""],
        ["Flight ÷ Ground transport", "", f"{round(250000 / t['total_co2_g'])}x", "", "", "", ""],
    ])

    ws.update(range_name="A1", values=rows)
    ws.format("A1", {"textFormat": {"bold": True, "fontSize": 14}})
    ws.format("A4", {"textFormat": {"bold": True, "fontSize": 12}})
    ws.format("A5:C5", {"textFormat": {"bold": True}, "backgroundColor": {"red": 0.95, "green": 0.95, "blue": 0.95}})
    ws.format("A14", {"textFormat": {"bold": True, "fontSize": 12}})
    ws.format("A15:G15", {"textFormat": {"bold": True}, "backgroundColor": {"red": 0.9, "green": 0.95, "blue": 0.9}})
    ws.columns_auto_resize(0, 7)


def setup_packing_tab(sh):
    """Create a packing/prep checklist tab."""
    ws = sh.add_worksheet(title="Pre-Trip Checklist", rows=40, cols=5)

    rows = [
        ["PRE-TRIP CHECKLIST"],
        [""],
        ["Done?", "Category", "Item", "Notes"],
        ["☐", "Apps", "Amap (高德地图)", "Offline maps for Shanghai + Suzhou"],
        ["☐", "Apps", "Dianping (大众点评)", "Restaurant reviews"],
        ["☐", "Apps", "WeChat (微信)", "Communication in China"],
        ["☐", "Apps", "Alipay (支付宝)", "Mobile payments"],
        ["☐", "Apps", "VPN (ExpressVPN/Astrill)", "Test before departure"],
        ["☐", "Transport", "Book Suzhou HSR tickets", "Via 12306 app or Trip.com"],
        ["☐", "Transport", "Shanghai metro card / Alipay transit", "Load credit"],
        ["☐", "Offline", "Download Amap offline maps", "Shanghai + Suzhou"],
        ["☐", "Offline", "Export QGIS PDF maps (Day 1-6)", "offline/ folder"],
        ["☐", "Offline", "Pre-load web map on phone", "Hotel WiFi + VPN"],
        ["☐", "Offline", "Print hotel address in Chinese", "Pocket card"],
        ["☐", "Documents", "Passport", "Check validity > 6 months"],
        ["☐", "Documents", "China visa (if required)", "Check requirements"],
        ["☐", "Documents", "Hotel booking confirmation", "Chinese + English"],
        ["☐", "Documents", "Travel insurance", ""],
        ["☐", "GIS Project", "All POIs have day assignments", "Check data/poi/ files"],
        ["☐", "GIS Project", "Web map deployed and tested", "Test on phone"],
        ["☐", "GIS Project", "CO2 calculator run", "tools/co2-calculator.py"],
        ["☐", "GIS Project", "Story map template ready", "web/story-template.html"],
    ]

    ws.update(range_name="A1", values=rows)
    ws.format("A1", {"textFormat": {"bold": True, "fontSize": 14}})
    ws.format("A3:D3", {"textFormat": {"bold": True}, "backgroundColor": {"red": 1.0, "green": 0.95, "blue": 0.9}})
    ws.columns_auto_resize(0, 4)


# ============================================================
# MAIN
# ============================================================

def main():
    print("Authenticating...")
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    gc = gspread.authorize(creds)

    print("Loading project data...")
    pois = load_pois()
    routes = load_routes()
    co2 = load_co2_summary()
    print(f"  {len(pois)} POIs, {sum(len(v) for v in routes.values())} route segments")

    print("Creating Google Sheet...")
    sh = create_sheet(gc)

    print("Building Overview tab...")
    setup_overview_tab(sh, pois, routes, co2)

    for day in range(1, 7):
        print(f"Building Day {day} tab...")
        setup_day_tab(sh, day, pois, routes, co2)

    print("Building All POIs tab...")
    setup_all_pois_tab(sh, pois)

    print("Building CO2 Analysis tab...")
    setup_co2_tab(sh, co2)

    print("Building Pre-Trip Checklist tab...")
    setup_packing_tab(sh)

    print(f"\nDone! Sheet URL: {sh.url}")
    print(f"Shared with: {SHARE_WITH_EMAIL}")


if __name__ == "__main__":
    main()
