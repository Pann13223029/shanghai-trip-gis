#!/usr/bin/env python3
"""
Rebuild all Day tabs with the expert-panel-designed layout:
- 8-column itinerary (TIME, ACTIVITY, LOCATION, TRANSPORT, COST, DIST, NOTES, STATUS)
- MORNING / LUNCH / AFTERNOON / DINNER / EVENING sections
- Eco Scorecard side panel with CO2 formulas
- Transport conditional formatting
- POI reference sorted by priority then sustainability score
- Pre-filled day context, eco tips, rain plan
"""

import json
import time
import gspread
from gspread.utils import rowcol_to_a1
from google.oauth2.service_account import Credentials
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
SERVICE_ACCOUNT_FILE = PROJECT_ROOT / "service-account.json"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ygvPoBHYxhrNQqCGjlNI6srOgTMV1-VkkNM43lVzkEg/edit"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

DAY_CONFIG = {
    1: {
        "theme": "Arrival & The Bund",
        "start": "Pudong Airport",
        "end": "People's Square area",
        "eco_tip": "Metro from PVG saves 80% CO2 vs taxi (40km!)",
        "start_time": "14:00",
        "lunch_time": "—",
        "dinner_time": "18:30",
    },
    2: {
        "theme": "Old Town & French Concession",
        "start": "People's Square",
        "end": "Xintiandi area",
        "eco_tip": "Both areas today are best explored on foot — 0g CO2",
        "start_time": "08:30",
        "lunch_time": "12:00",
        "dinner_time": "18:00",
    },
    3: {
        "theme": "Pudong Skyline",
        "start": "People's Square",
        "end": "Lujiazui / Pudong",
        "eco_tip": "Lujiazui is fully walkable once you arrive by metro — one ride, then walk all day",
        "start_time": "09:00",
        "lunch_time": "12:00",
        "dinner_time": "18:00",
    },
    4: {
        "theme": "Culture & Art",
        "start": "People's Square",
        "end": "TBD",
        "eco_tip": "Check opening days — some museums close Mondays",
        "start_time": "09:00",
        "lunch_time": "12:00",
        "dinner_time": "18:00",
    },
    5: {
        "theme": "Explore & Free Day",
        "start": "People's Square",
        "end": "TBD",
        "eco_tip": "Free day — explore by metro + walking for lowest impact",
        "start_time": "09:00",
        "lunch_time": "12:00",
        "dinner_time": "18:00",
    },
    6: {
        "theme": "Suzhou Day Trip",
        "start": "People's Square",
        "end": "People's Square",
        "eco_tip": "HSR to Suzhou = 6g/km — the greenest intercity transport option in China",
        "start_time": "07:30",
        "lunch_time": "12:30",
        "dinner_time": "18:30",
    },
}

PRIORITY_ORDER = {"must-visit": 0, "nice-to-have": 1, "optional": 2}

# Colors
BLUE_HEADER = {"red": 0.85, "green": 0.89, "blue": 0.95}
GRAY_SECTION = {"red": 0.91, "green": 0.91, "blue": 0.91}
YELLOW_MEAL = {"red": 1.0, "green": 0.97, "blue": 0.88}
GREEN_ECO = {"red": 0.84, "green": 0.96, "blue": 0.84}
SAGE_POI = {"red": 0.89, "green": 0.94, "blue": 0.85}
GRAY_TOTALS = {"red": 0.94, "green": 0.94, "blue": 0.94}
WHITE = {"red": 1, "green": 1, "blue": 1}


def load_pois():
    poi_dir = PROJECT_ROOT / "data" / "poi"
    all_pois = []
    for f in sorted(poi_dir.glob("*.geojson")):
        with open(f, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            for feat in data.get("features", []):
                all_pois.append(feat["properties"])
    return all_pois


def get_day_pois(pois, day):
    day_pois = [p for p in pois if p.get("day") == day]
    return sorted(day_pois, key=lambda p: (
        PRIORITY_ORDER.get(p.get("priority", "optional"), 9),
        -(p.get("sustainability_score") or 0)
    ))


def build_day_sheet(sh, ws, day, pois, config):
    """Build a single day sheet with the new layout."""
    ws.clear()
    day_pois = get_day_pois(pois, day)
    c = config

    # ── SECTION 1: Header (rows 1-3) ──
    rows = [
        [f"DAY {day} — {c['theme']}", "", "", "", "", "", "", ""],
        [f"Date: ___", f"Start: {c['start']}", "", f"End: {c['end']}", "", f"Weather: ___", "", ""],
        [f"Eco tip: {c['eco_tip']}", "", "", "", "", "", "", ""],
        # ── SECTION 2: Itinerary Headers (row 4) ──
        ["TIME", "ACTIVITY", "LOCATION", "TRANSPORT", "COST (CNY)", "DIST (km)", "NOTES", "STATUS"],
        # ── MORNING section (row 5) ──
        ["MORNING", "", "", "", "", "", "", ""],
        # Activity rows 6-8
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        # LUNCH (row 9)
        [c["lunch_time"], "LUNCH", "(find locally / planned restaurant)", "", "~80", "", "", ""],
        # AFTERNOON section (row 10)
        ["AFTERNOON", "", "", "", "", "", "", ""],
        # Activity rows 11-13
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        # DINNER (row 14)
        [c["dinner_time"], "DINNER", "(find locally / planned restaurant)", "", "~100", "", "", ""],
        # EVENING section (row 15)
        ["EVENING", "", "", "", "", "", "", ""],
        # Activity rows 16-17
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        # Spacer (row 18)
        ["", "", "", "", "", "", "", ""],
        # TOTALS (row 19)
        ["", "TOTALS", "", "",
         "=SUM(E6:E8,E9,E11:E13,E14,E16:E17)",
         "=SUM(F6:F8,F9,F11:F13,F14,F16:F17)",
         "",
         '=COUNTA(H6:H8,H11:H13,H16:H17)&" of "&COUNTA(B6:B8,B11:B13,B16:B17)'],
        # Spacer (row 20)
        ["", "", "", "", "", "", "", ""],
        # Rain plan (row 21)
        ["Rain plan: ___", "", "", "", "", "", "", ""],
        # Spacer (row 22)
        ["", "", "", "", "", "", "", ""],
    ]

    # ── ECO SCORECARD (cols J-L, rows 4-18) ──
    # We'll build these as extra columns on existing rows
    # Pad rows to col L (12 columns = A-L, index 0-11)
    for i in range(len(rows)):
        while len(rows[i]) < 12:
            rows[i].append("")

    # Row 4 (index 3): Scorecard header
    rows[3][9] = "ECO SCORECARD"
    rows[3][10] = ""
    rows[3][11] = ""

    # Rows 5-11 (index 4-10): CO2 section
    rows[4][9] = "Transport CO2"
    rows[4][10] = ""
    rows[4][11] = ""

    rows[5][9] = "Walking dist"
    rows[5][10] = '=SUMPRODUCT((D6:D17="walking")*F6:F17)'
    rows[5][11] = "km"

    rows[6][9] = "Metro/bus dist"
    rows[6][10] = '=SUMPRODUCT((D6:D17="metro")*F6:F17)+SUMPRODUCT((D6:D17="bus")*F6:F17)'
    rows[6][11] = "km"

    rows[7][9] = "Taxi dist"
    rows[7][10] = '=SUMPRODUCT((D6:D17="taxi")*F6:F17)+SUMPRODUCT((D6:D17="e-taxi")*F6:F17)'
    rows[7][11] = "km"

    rows[8][9] = "Total CO2"
    rows[8][10] = '=K7*29+K8*120+SUMPRODUCT((D6:D17="train")*F6:F17)*6+SUMPRODUCT((D6:D17="maglev")*F6:F17)*95+SUMPRODUCT((D6:D17="e-taxi")*F6:F17)*45'
    rows[8][11] = "grams"

    rows[9][9] = "If all taxi"
    rows[9][10] = "=SUM(F6:F17)*120"
    rows[9][11] = "grams"

    rows[10][9] = "CO2 saved"
    rows[10][10] = '=IF(K10>0,ROUND((1-K9/K10)*100,0)&"%","—")'
    rows[10][11] = ""

    # Rows 12-17 (index 11-16): Daily stats
    rows[11][9] = ""
    rows[12][9] = "Daily Stats"
    rows[12][10] = ""
    rows[12][11] = ""

    rows[13][9] = "Activities"
    rows[13][10] = "=COUNTA(B6:B8,B11:B13,B16:B17)"
    rows[13][11] = ""

    rows[14][9] = "Total cost"
    rows[14][10] = "=E19"
    rows[14][11] = "CNY"

    rows[15][9] = "Total distance"
    rows[15][10] = "=F19"
    rows[15][11] = "km"

    rows[16][9] = "Visited"
    rows[16][10] = '=COUNTIF(H6:H17,"visited")'
    rows[16][11] = ""

    rows[17][9] = "Completion"
    rows[17][10] = '=IF(K14>0,ROUND(K17/K14*100,0)&"%","—")'
    rows[17][11] = ""

    # ── SECTION 4: POI Reference ──
    poi_header_idx = len(rows)
    rows.append(["AVAILABLE POIs FOR THIS DAY", "", "", "", "", "", "", "", "", "", "", ""])
    rows.append(["NAME", "CHINESE", "CATEGORY", "HOURS", "~MINS", "~COST", "SCORE", "INDOOR?", "", "", "", ""])

    for p in day_pois:
        score = p.get("sustainability_score")
        score_str = f"{score}/12" if score is not None else "N/A"
        rows.append([
            p.get("name_en", ""),
            p.get("name_cn", ""),
            p.get("category", ""),
            p.get("opening_hours", ""),
            p.get("est_duration_min", ""),
            p.get("est_cost_cny", ""),
            score_str,
            "Indoor" if not p.get("weather_sensitive") else "Outdoor",
            "", "", "", "",
        ])

    # Emission factors reference
    rows.append(["", "", "", "", "", "", "", "", "", "", "", ""])
    rows.append(["EMISSION FACTORS (g CO2/km/person): walking=0 | metro=29 | bus=65 | taxi=120 | e-taxi=45 | train=6 | maglev=95",
                 "", "", "", "", "", "", "", "", "", "", ""])
    rows.append(["Score = transit(0-3) + heritage(0-3) + walkability(0-3) + env.sensitivity(0-3). Max 12. Community impact is qualitative.",
                 "", "", "", "", "", "", "", "", "", "", ""])

    # ── WRITE ALL DATA ──
    ws.update(range_name="A1", values=rows, value_input_option="USER_ENTERED")

    # ── FORMATTING ──

    # Title (row 1)
    ws.merge_cells("A1:H1")
    ws.format("A1:H1", {"textFormat": {"bold": True, "fontSize": 16}})

    # Context row (row 2)
    ws.format("A2:H2", {"textFormat": {"fontSize": 10, "foregroundColorStyle": {"rgbColor": {"red": 0.4, "green": 0.4, "blue": 0.4}}}})

    # Eco tip (row 3)
    ws.merge_cells("A3:H3")
    ws.format("A3:H3", {"textFormat": {"italic": True, "fontSize": 10, "foregroundColorStyle": {"rgbColor": {"red": 0.18, "green": 0.49, "blue": 0.2}}}})

    # Itinerary header (row 4)
    ws.format("A4:H4", {
        "textFormat": {"bold": True},
        "backgroundColor": BLUE_HEADER,
        "borders": {"bottom": {"style": "SOLID", "colorStyle": {"rgbColor": {"red": 0.5, "green": 0.5, "blue": 0.5}}}}
    })

    # Section labels: MORNING (5), AFTERNOON (10), EVENING (15)
    for row in [5, 10, 15]:
        ws.merge_cells(f"A{row}:H{row}")
        ws.format(f"A{row}:H{row}", {
            "textFormat": {"bold": True, "fontSize": 10},
            "backgroundColor": GRAY_SECTION,
            "horizontalAlignment": "CENTER",
        })

    # Meal rows: LUNCH (9), DINNER (14)
    for row in [9, 14]:
        ws.format(f"A{row}:H{row}", {
            "textFormat": {"italic": True},
            "backgroundColor": YELLOW_MEAL,
        })

    # TOTALS row (19)
    ws.format("A19:H19", {
        "textFormat": {"bold": True},
        "backgroundColor": GRAY_TOTALS,
        "borders": {"top": {"style": "SOLID", "colorStyle": {"rgbColor": {"red": 0.4, "green": 0.4, "blue": 0.4}}}}
    })

    # Rain plan (21)
    ws.merge_cells("A21:H21")
    ws.format("A21:H21", {"textFormat": {"italic": True, "fontSize": 10, "foregroundColorStyle": {"rgbColor": {"red": 0.4, "green": 0.4, "blue": 0.6}}}})

    # Eco Scorecard header (J4)
    ws.merge_cells("J4:L4")
    ws.format("J4:L4", {
        "textFormat": {"bold": True, "fontSize": 11},
        "backgroundColor": GREEN_ECO,
        "horizontalAlignment": "CENTER",
    })

    # Eco scorecard labels
    ws.format("J5:J18", {"textFormat": {"fontSize": 10}})
    ws.format("J5", {"textFormat": {"bold": True, "fontSize": 10}})
    ws.format("J13", {"textFormat": {"bold": True, "fontSize": 10}})

    # Scorecard border
    ws.format("J4:L18", {
        "borders": {
            "top": {"style": "SOLID"},
            "bottom": {"style": "SOLID"},
            "left": {"style": "SOLID"},
            "right": {"style": "SOLID"},
        }
    })

    # POI reference header
    poi_h1 = poi_header_idx + 1
    poi_h2 = poi_header_idx + 2
    ws.merge_cells(f"A{poi_h1}:H{poi_h1}")
    ws.format(f"A{poi_h1}:H{poi_h1}", {"textFormat": {"bold": True, "fontSize": 13}})
    ws.format(f"A{poi_h2}:H{poi_h2}", {
        "textFormat": {"bold": True},
        "backgroundColor": SAGE_POI,
        "borders": {"bottom": {"style": "SOLID"}}
    })

    # Footer references (italic, small, gray)
    last_rows = len(rows)
    ws.merge_cells(f"A{last_rows - 1}:H{last_rows - 1}")
    ws.merge_cells(f"A{last_rows}:H{last_rows}")
    ws.format(f"A{last_rows - 1}:H{last_rows}", {
        "textFormat": {"italic": True, "fontSize": 9, "foregroundColorStyle": {"rgbColor": {"red": 0.5, "green": 0.5, "blue": 0.5}}}
    })

    # Freeze header row
    ws.freeze(rows=4)

    # Column widths
    try:
        requests = [
            {"updateDimensionProperties": {"range": {"sheetId": ws.id, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 1}, "properties": {"pixelSize": 70}, "fields": "pixelSize"}},
            {"updateDimensionProperties": {"range": {"sheetId": ws.id, "dimension": "COLUMNS", "startIndex": 1, "endIndex": 2}, "properties": {"pixelSize": 130}, "fields": "pixelSize"}},
            {"updateDimensionProperties": {"range": {"sheetId": ws.id, "dimension": "COLUMNS", "startIndex": 2, "endIndex": 3}, "properties": {"pixelSize": 220}, "fields": "pixelSize"}},
            {"updateDimensionProperties": {"range": {"sheetId": ws.id, "dimension": "COLUMNS", "startIndex": 3, "endIndex": 4}, "properties": {"pixelSize": 90}, "fields": "pixelSize"}},
            {"updateDimensionProperties": {"range": {"sheetId": ws.id, "dimension": "COLUMNS", "startIndex": 4, "endIndex": 5}, "properties": {"pixelSize": 75}, "fields": "pixelSize"}},
            {"updateDimensionProperties": {"range": {"sheetId": ws.id, "dimension": "COLUMNS", "startIndex": 5, "endIndex": 6}, "properties": {"pixelSize": 70}, "fields": "pixelSize"}},
            {"updateDimensionProperties": {"range": {"sheetId": ws.id, "dimension": "COLUMNS", "startIndex": 6, "endIndex": 7}, "properties": {"pixelSize": 200}, "fields": "pixelSize"}},
            {"updateDimensionProperties": {"range": {"sheetId": ws.id, "dimension": "COLUMNS", "startIndex": 7, "endIndex": 8}, "properties": {"pixelSize": 80}, "fields": "pixelSize"}},
            {"updateDimensionProperties": {"range": {"sheetId": ws.id, "dimension": "COLUMNS", "startIndex": 8, "endIndex": 9}, "properties": {"pixelSize": 20}, "fields": "pixelSize"}},
            {"updateDimensionProperties": {"range": {"sheetId": ws.id, "dimension": "COLUMNS", "startIndex": 9, "endIndex": 12}, "properties": {"pixelSize": 100}, "fields": "pixelSize"}},
        ]
        sh.batch_update({"requests": requests})
    except Exception as e:
        print(f"    (column width warning: {e})")

    # Data validation: TRANSPORT dropdown (D6:D17)
    try:
        ws.set_data_validation("D6:D17", gspread.DataValidationRule(
            gspread.BooleanCondition("ONE_OF_LIST", ["walking", "metro", "bus", "taxi", "e-taxi", "train", "maglev"]),
            showCustomUi=True
        ))
    except Exception as e:
        print(f"    (transport validation warning: {e})")

    # Data validation: STATUS dropdown (H6:H17)
    try:
        ws.set_data_validation("H6:H17", gspread.DataValidationRule(
            gspread.BooleanCondition("ONE_OF_LIST", ["planned", "confirmed", "visited", "skipped", "moved"]),
            showCustomUi=True
        ))
    except Exception as e:
        print(f"    (status validation warning: {e})")

    # Conditional formatting for transport colors
    try:
        transport_range = {"sheetId": ws.id, "startRowIndex": 5, "endRowIndex": 17, "startColumnIndex": 3, "endColumnIndex": 4}
        cond_rules = [
            {"addConditionalFormatRule": {"rule": {"ranges": [transport_range], "booleanRule": {"condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": "walking"}]}, "format": {"backgroundColor": {"red": 0.84, "green": 0.96, "blue": 0.84}}}}, "index": 0}},
            {"addConditionalFormatRule": {"rule": {"ranges": [transport_range], "booleanRule": {"condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": "train"}]}, "format": {"backgroundColor": {"red": 0.84, "green": 0.96, "blue": 0.84}}}}, "index": 1}},
            {"addConditionalFormatRule": {"rule": {"ranges": [transport_range], "booleanRule": {"condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": "metro"}]}, "format": {"backgroundColor": {"red": 0.84, "green": 0.91, "blue": 0.96}}}}, "index": 2}},
            {"addConditionalFormatRule": {"rule": {"ranges": [transport_range], "booleanRule": {"condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": "bus"}]}, "format": {"backgroundColor": {"red": 0.84, "green": 0.91, "blue": 0.96}}}}, "index": 3}},
            {"addConditionalFormatRule": {"rule": {"ranges": [transport_range], "booleanRule": {"condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": "taxi"}]}, "format": {"backgroundColor": {"red": 0.99, "green": 0.91, "blue": 0.82}}}}, "index": 4}},
            {"addConditionalFormatRule": {"rule": {"ranges": [transport_range], "booleanRule": {"condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": "e-taxi"}]}, "format": {"backgroundColor": {"red": 0.91, "green": 0.96, "blue": 0.84}}}}, "index": 5}},
        ]
        sh.batch_update({"requests": cond_rules})
    except Exception as e:
        print(f"    (conditional formatting warning: {e})")


def main():
    print("Authenticating...")
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_url(SHEET_URL)

    print("Loading POI data...")
    pois = load_pois()

    START_FROM = int(input("Start from day (1-6, default 1): ") or "1")
    for day in range(START_FROM, 7):
        config = DAY_CONFIG[day]
        tab_name = f"Day {day}"
        print(f"Building {tab_name} — {config['theme']}...")

        try:
            ws = sh.worksheet(tab_name)
        except gspread.exceptions.WorksheetNotFound:
            ws = sh.add_worksheet(title=tab_name, rows=60, cols=16)

        build_day_sheet(sh, ws, day, pois, config)
        day_pois = get_day_pois(pois, day)
        print(f"  Done: {len(day_pois)} POIs, eco scorecard, dropdowns, conditional formatting")
        if day < 6:
            print("  Waiting 65s for API rate limit...")
            time.sleep(65)

    print(f"\nAll 6 day tabs rebuilt!")
    print(f"Sheet: {sh.url}")


if __name__ == "__main__":
    main()
