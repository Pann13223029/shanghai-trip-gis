#!/usr/bin/env python3
"""Re-create day tabs with empty itinerary frames (headers + formatting, no data)."""

import json
import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
SERVICE_ACCOUNT_FILE = PROJECT_ROOT / "service-account.json"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ygvPoBHYxhrNQqCGjlNI6srOgTMV1-VkkNM43lVzkEg/edit"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

DAY_THEMES = {
    1: "Arrival & The Bund",
    2: "Old Town & French Concession",
    3: "Pudong Skyline",
    4: "Culture & Art",
    5: "Explore & Free Day",
    6: "Suzhou Day Trip",
}

# Load POIs to keep the POI details section populated
def load_pois():
    poi_dir = PROJECT_ROOT / "data" / "poi"
    all_pois = []
    for f in sorted(poi_dir.glob("*.geojson")):
        with open(f, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            for feat in data.get("features", []):
                all_pois.append(feat["properties"])
    return all_pois

pois = load_pois()

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
gc = gspread.authorize(creds)
sh = gc.open_by_url(SHEET_URL)

for day in range(1, 7):
    tab_name = f"Day {day}"
    try:
        ws = sh.worksheet(tab_name)
        ws.clear()
        print(f"  Clearing {tab_name}...")
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet(title=tab_name, rows=60, cols=12)
        print(f"  Creating {tab_name}...")

    theme = DAY_THEMES.get(day, "")
    day_pois = sorted(
        [p for p in pois if p.get("day") == day],
        key=lambda p: p.get("id", "")
    )

    # Build empty itinerary frame
    rows = [
        [f"DAY {day} — {theme}"],
        [""],
        ["TIME", "ACTIVITY", "LOCATION (EN)", "LOCATION (CN)", "TRANSPORT", "DISTANCE", "DURATION", "CO2", "COST (CNY)", "NOTES"],
        # 12 empty rows for the user to fill in
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        [""],
        ["", "TOTALS", "", "", "", "", "", "", "", ""],
        [""],
        [""],
        ["DAY'S POINTS OF INTEREST"],
        ["ID", "Name (EN)", "Name (CN)", "Category", "Priority", "Duration", "Cost (CNY)", "Hours", "Weather", "Sustainability Score", "Notes"],
    ]

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
            (p.get("notes", "") or "")[:100],
        ])

    ws.update(range_name="A1", values=rows)

    # Format
    ws.format("A1", {"textFormat": {"bold": True, "fontSize": 14}})
    ws.format("A3:J3", {
        "textFormat": {"bold": True},
        "backgroundColor": {"red": 0.85, "green": 0.92, "blue": 1.0}
    })
    ws.format("B17:J17", {"textFormat": {"bold": True}})

    poi_header_row = 20 + 1  # row 21
    ws.format(f"A{poi_header_row}:K{poi_header_row}", {
        "textFormat": {"bold": True},
        "backgroundColor": {"red": 0.9, "green": 0.95, "blue": 0.9}
    })

    ws.columns_auto_resize(0, 11)
    print(f"  {tab_name}: Frame rebuilt with {len(day_pois)} POIs, itinerary empty for you to fill")

print("\nDone. All day tabs have empty itinerary frames ready to fill.")
