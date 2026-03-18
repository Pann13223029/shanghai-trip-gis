#!/usr/bin/env python3
"""Clear the day tab titles and itinerary timelines, keeping only POI details."""

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

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
gc = gspread.authorize(creds)
sh = gc.open_by_url(SHEET_URL)

for day in range(1, 7):
    tab_name = f"Day {day}"
    try:
        ws = sh.worksheet(tab_name)
        all_values = ws.get_all_values()

        # Find where "DAY'S POINTS OF INTEREST" row starts
        poi_header_row = None
        for i, row in enumerate(all_values):
            if any("POINTS OF INTEREST" in str(cell) for cell in row):
                poi_header_row = i
                break

        if poi_header_row is not None:
            # Clear everything above the POI section (the itinerary timeline)
            # Row 1 = title, rows 2..poi_header_row = itinerary
            ws.batch_clear([f"A1:K{poi_header_row}"])
            print(f"  {tab_name}: Cleared rows 1-{poi_header_row} (itinerary + title)")
        else:
            # No POI section found — clear everything
            ws.clear()
            print(f"  {tab_name}: Cleared all (no POI section found)")

    except gspread.exceptions.WorksheetNotFound:
        print(f"  {tab_name}: Tab not found, skipping")

print("\nDone. Day tab titles and itineraries cleared.")
