#!/usr/bin/env python3
"""
Rebuild the 4 non-day tabs: Overview, All POIs, CO2 Analysis, Pre-Trip Checklist.
Implements the expert panel consensus design.
"""

import json
import time
import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
SERVICE_ACCOUNT_FILE = PROJECT_ROOT / "service-account.json"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ygvPoBHYxhrNQqCGjlNI6srOgTMV1-VkkNM43lVzkEg/edit"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

PRIORITY_ORDER = {"must-visit": 0, "nice-to-have": 1, "optional": 2}
CATEGORY_COLORS = {
    "landmark":      {"red": 0.99, "green": 0.87, "blue": 0.87},
    "food":          {"red": 1.0,  "green": 0.94, "blue": 0.88},
    "cultural":      {"red": 0.88, "green": 0.94, "blue": 1.0},
    "nature":        {"red": 0.88, "green": 1.0,  "blue": 0.88},
    "shopping":      {"red": 0.94, "green": 0.88, "blue": 1.0},
    "transport":     {"red": 0.94, "green": 0.94, "blue": 0.94},
    "accommodation": {"red": 1.0,  "green": 0.98, "blue": 0.88},
}

DAY_THEMES = {1: "Arrival & The Bund", 2: "Old Town & French Concession", 3: "Pudong Skyline",
              4: "Culture & Art", 5: "Explore & Free Day", 6: "Suzhou Day Trip"}


def load_pois():
    all_pois = []
    for f in sorted((PROJECT_ROOT / "data" / "poi").glob("*.geojson")):
        with open(f, "r", encoding="utf-8") as fh:
            for feat in json.load(fh).get("features", []):
                all_pois.append(feat["properties"])
    return all_pois


def load_co2():
    f = PROJECT_ROOT / "data" / "analysis" / "co2-summary.json"
    if f.exists():
        with open(f, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return None


def load_routes():
    routes = {}
    for day in range(1, 7):
        f = PROJECT_ROOT / "data" / "routes" / f"day-{day}.geojson"
        if f.exists():
            with open(f, "r", encoding="utf-8") as fh:
                data = json.load(fh)
                if data.get("features"):
                    routes[day] = data["features"]
    return routes


# ============================================================
# TAB 1: OVERVIEW
# ============================================================

def build_overview(sh, pois, co2, routes):
    print("Building Overview...")
    try:
        ws = sh.worksheet("Overview")
        ws.clear()
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet(title="Overview", rows=25, cols=12)

    t = co2["trip_total"] if co2 else {}
    assigned = len([p for p in pois if p.get("day")])
    must_visit = len([p for p in pois if p.get("priority") == "must-visit"])

    rows = [
        # Row 1: Title
        ["SHANGHAI & SUZHOU TRIP 2026", "", "", "", "", "",
         "QUICK REFERENCE", "", "", ""],
        # Row 2: Sustainability banner
        [f"87% CO2 saved | {t.get('total_co2_kg', '?')} kg total | Metro + walking + HSR for 97% of distance", "", "", "", "", "",
         "Hotel:", "___", "", ""],
        # Row 3: Trip dates
        ["Trip dates: ___ to ___, 2026", "", "", "", "", "",
         "Hotel (CN):", "___", "", ""],
        # Row 4: blank
        ["", "", "", "", "", "",
         "Check-in:", "___", "Check-out:", "___"],
        # Row 5: Progress
        [f"TRIP PROGRESS: {assigned} of {len(pois)} POIs assigned | {must_visit} must-visit", "", "", "", "", "",
         "Emergency:", "Police 110 | Ambulance 120", "", ""],
        # Row 6: blank
        ["", "", "", "", "", "",
         "Embassy:", "+86-XXX-XXXX", "", ""],
        # Row 7: Table header
        ["DAY", "THEME", "POIs", "TOP MODE", "CO2 SAVED", "STATUS",
         "VPN:", "___", "", ""],
    ]

    # Day rows 8-13
    for day in range(1, 7):
        day_pois = [p for p in pois if p.get("day") == day]
        day_co2_saved = ""
        top_mode = ""
        if co2:
            for d in co2.get("days", []):
                if d["day"] == day:
                    day_co2_saved = f"{d['co2_saved_vs_taxi_pct']}%"
                    top_dist = 0
                    for mode, data in d.get("mode_breakdown", {}).items():
                        if data["distance_km"] > top_dist:
                            top_dist = data["distance_km"]
                            top_mode = mode
        rows.append([
            f"Day {day}", DAY_THEMES.get(day, ""), len(day_pois),
            top_mode or "—", day_co2_saved or "—", "",
            "", "", "", "",
        ])

    # Footer
    rows.extend([
        ["", "", "", "", "", "", "", "", "", ""],
        ["Methodology: Shanghai-specific emission factors. See CO2 Analysis tab and docs/sustainability-methodology.md", "", "", "", "", "", "", "", "", ""],
        ["Live Map: https://pann13223029.github.io/shanghai-trip-gis/", "",
         "GitHub: https://github.com/Pann13223029/shanghai-trip-gis", "", "", "", "", "", "", ""],
    ])

    ws.update(range_name="A1", values=rows, value_input_option="USER_ENTERED")

    # Formatting
    ws.merge_cells("A1:E1")
    ws.format("A1:E1", {"textFormat": {"bold": True, "fontSize": 16}})

    ws.merge_cells("A2:E2")
    ws.format("A2:E2", {"textFormat": {"bold": True, "fontSize": 11},
                         "backgroundColor": {"red": 0.84, "green": 0.96, "blue": 0.84}})

    ws.merge_cells("A3:E3")
    ws.format("A3:E3", {"textFormat": {"italic": True, "fontSize": 10}})

    ws.merge_cells("A5:E5")
    ws.format("A5:E5", {"textFormat": {"bold": True, "fontSize": 10}})

    # Quick ref box
    ws.merge_cells("G1:J1")
    ws.format("G1:J7", {"backgroundColor": {"red": 0.89, "green": 0.94, "blue": 0.99}})
    ws.format("G1:G7", {"textFormat": {"bold": True, "fontSize": 10}})

    # Table header
    ws.format("A7:F7", {"textFormat": {"bold": True},
                         "backgroundColor": {"red": 0.85, "green": 0.88, "blue": 0.93}})
    ws.freeze(rows=7)

    # Status dropdown
    sid = ws.id
    requests = [{
        "setDataValidation": {
            "range": {"sheetId": sid, "startRowIndex": 7, "endRowIndex": 13, "startColumnIndex": 5, "endColumnIndex": 6},
            "rule": {"condition": {"type": "ONE_OF_LIST", "values": [{"userEnteredValue": v} for v in ["planning", "confirmed", "in-progress", "done"]]},
                     "showCustomUi": True}
        }
    }]
    sh.batch_update({"requests": requests})

    # Footer
    ws.merge_cells(f"A{len(rows)-1}:F{len(rows)-1}")
    ws.format(f"A{len(rows)-1}:F{len(rows)}", {"textFormat": {"italic": True, "fontSize": 9,
              "foregroundColorStyle": {"rgbColor": {"red": 0.5, "green": 0.5, "blue": 0.5}}}})

    ws.columns_auto_resize(0, 10)
    print("  Done")


# ============================================================
# TAB 2: ALL POIs
# ============================================================

def build_all_pois(sh, pois):
    print("Building All POIs...")
    try:
        ws = sh.worksheet("All POIs")
        ws.clear()
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet(title="All POIs", rows=60, cols=16)

    sorted_pois = sorted(pois, key=lambda p: (
        p.get("day") or 99,
        PRIORITY_ORDER.get(p.get("priority", "optional"), 9),
        -(p.get("sustainability_score") or 0)
    ))

    must = len([p for p in pois if p.get("priority") == "must-visit"])
    nice = len([p for p in pois if p.get("priority") == "nice-to-have"])
    opt = len([p for p in pois if p.get("priority") == "optional"])
    scores = [p.get("sustainability_score") for p in pois if p.get("sustainability_score") is not None]
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0

    rows = [
        ["ALL POINTS OF INTEREST", "", "", "", "", "", "", "", "", "", "", "",
         "", "LEGEND"],
        [f"{len(pois)} POIs | Avg score: {avg_score}/12 | {must} must-visit, {nice} nice-to-have, {opt} optional",
         "", "", "", "", "", "", "", "", "", "", "",
         "", "landmark"],
        ["ID", "NAME (EN)", "NAME (CN)", "CATEGORY", "DAY", "PRIORITY",
         "MINS", "COST", "HOURS", "SCORE", "INDOOR?", "STATUS",
         "", "food"],
    ]

    # Legend continues in col N
    legend_cats = ["cultural", "nature", "shopping", "transport"]

    for i, p in enumerate(sorted_pois):
        score = p.get("sustainability_score")
        score_str = f"{score}/12" if score is not None else "—"
        indoor = "Indoor" if not p.get("weather_sensitive") else "Outdoor"
        legend_val = legend_cats[i] if i < len(legend_cats) else ""
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
            score_str,
            indoor,
            "",
            "",
            legend_val,
        ])

    ws.update(range_name="A1", values=rows, value_input_option="USER_ENTERED")

    # Formatting
    ws.merge_cells("A1:L1")
    ws.format("A1:L1", {"textFormat": {"bold": True, "fontSize": 14}})
    ws.merge_cells("A2:L2")
    ws.format("A2:L2", {"textFormat": {"italic": True, "fontSize": 10}})
    ws.format("A3:L3", {"textFormat": {"bold": True},
                         "backgroundColor": {"red": 0.94, "green": 0.94, "blue": 0.94}})
    ws.format("N1", {"textFormat": {"bold": True, "fontSize": 10}})
    ws.freeze(rows=3)

    # Chinese name column larger font
    ws.format(f"C4:C{len(rows)}", {"textFormat": {"fontSize": 12}})

    # Status dropdown
    sid = ws.id
    requests = [{
        "setDataValidation": {
            "range": {"sheetId": sid, "startRowIndex": 3, "endRowIndex": len(rows),
                      "startColumnIndex": 11, "endColumnIndex": 12},
            "rule": {"condition": {"type": "ONE_OF_LIST",
                     "values": [{"userEnteredValue": v} for v in ["planned", "confirmed", "visited", "skipped"]]},
                     "showCustomUi": True}
        }
    }]

    # Category color formatting
    for cat, color in CATEGORY_COLORS.items():
        requests.append({
            "addConditionalFormatRule": {"rule": {
                "ranges": [{"sheetId": sid, "startRowIndex": 3, "endRowIndex": len(rows),
                            "startColumnIndex": 3, "endColumnIndex": 4}],
                "booleanRule": {
                    "condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": cat}]},
                    "format": {"backgroundColor": color}
                }
            }, "index": 0}
        })

    # Sustainability score color formatting (col J = index 9)
    score_range = {"sheetId": sid, "startRowIndex": 3, "endRowIndex": len(rows),
                   "startColumnIndex": 9, "endColumnIndex": 10}
    requests.append({"addConditionalFormatRule": {"rule": {
        "ranges": [score_range],
        "booleanRule": {"condition": {"type": "TEXT_CONTAINS", "values": [{"userEnteredValue": "1"}]},
                        "format": {"backgroundColor": {"red": 0.84, "green": 0.96, "blue": 0.84}}}
    }, "index": 0}})

    # Legend colors
    for i, (cat, color) in enumerate(CATEGORY_COLORS.items()):
        row_idx = 1 + i  # N2, N3, N4...
        if row_idx < len(rows):
            requests.append({
                "repeatCell": {
                    "range": {"sheetId": sid, "startRowIndex": row_idx, "endRowIndex": row_idx + 1,
                              "startColumnIndex": 13, "endColumnIndex": 14},
                    "cell": {"userEnteredFormat": {"backgroundColor": color, "textFormat": {"fontSize": 9}}},
                    "fields": "userEnteredFormat(backgroundColor,textFormat)"
                }
            })

    sh.batch_update({"requests": requests})
    ws.columns_auto_resize(0, 14)
    print(f"  Done: {len(sorted_pois)} POIs")


# ============================================================
# TAB 3: CO2 ANALYSIS
# ============================================================

def build_co2(sh, co2):
    print("Building CO2 Analysis...")
    if not co2:
        print("  Skipped — no CO2 data")
        return

    try:
        ws = sh.worksheet("CO2 Analysis")
        ws.clear()
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet(title="CO2 Analysis", rows=50, cols=10)

    t = co2["trip_total"]

    # Compute mode split
    mode_totals = {}
    for d in co2.get("days", []):
        for mode, data in d.get("mode_breakdown", {}).items():
            if mode not in mode_totals:
                mode_totals[mode] = 0
            mode_totals[mode] += data["distance_km"]
    total_dist = t["total_distance_km"]
    mode_pcts = {m: round(d / total_dist * 100, 1) if total_dist > 0 else 0
                 for m, d in mode_totals.items()}

    flight_ratio = round(250000 / t["total_co2_g"]) if t["total_co2_g"] > 0 else "∞"

    rows = [
        ["TRANSPORT CO2 ANALYSIS", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        # Headline numbers
        [f"{t['total_co2_kg']} kg", "", f"{t['co2_saved_pct']}%", "", f"1/{flight_ratio}x", "", "", ""],
        ["Total trip CO2", "", "Saved vs all-taxi", "", "of a one-way flight", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        # Mode split
        ["MODE SPLIT", f"(% of {total_dist} km total)", "", "", "", "", "", ""],
    ]

    mode_row = []
    pct_row = []
    for mode in ["walking", "metro", "train", "taxi"]:
        pct = mode_pcts.get(mode, 0)
        km = mode_totals.get(mode, 0)
        mode_row.append(f"{mode}: {pct}%")
        pct_row.append(f"{km:.1f} km")
    rows.append(mode_row + ["", "", "", ""])
    rows.append(pct_row + ["", "", "", ""])

    rows.extend([
        ["", "", "", "", "", "", "", ""],
        # Context comparisons
        ["HOW DO WE COMPARE?", "", "", "", "", "", "", ""],
        ["Scenario", "", "CO2", "", "", "", "", ""],
        ["Our trip (ground transport)", "", f"{t['total_co2_kg']} kg", "", "", "", "", ""],
        ["Same trip, all by taxi", "", f"{t['all_taxi_co2_kg']} kg", "", "", "", "", ""],
        ["Shanghai commuter (6 days)", "", "3.5 kg", "", "", "", "", ""],
        ["International flight (one way)", "", "250 kg", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        # Daily breakdown
        ["DAILY BREAKDOWN", "", "", "", "", "", "", ""],
        ["DAY", "THEME", "DIST (km)", "CO2 (g)", "IF TAXI (g)", "SAVED", "TOP MODE", "NOTE"],
    ])

    for day in range(1, 7):
        found = False
        for d in co2.get("days", []):
            if d["day"] == day:
                top_mode = ""
                top_dist = 0
                for mode, data in d.get("mode_breakdown", {}).items():
                    if data["distance_km"] > top_dist:
                        top_dist = data["distance_km"]
                        top_mode = mode
                rows.append([
                    f"Day {day}", DAY_THEMES.get(day, ""), d["total_distance_km"],
                    d["total_co2_g"], d["all_taxi_co2_g"],
                    f"{d['co2_saved_vs_taxi_pct']}%", top_mode, ""
                ])
                found = True
                break
        if not found:
            rows.append([f"Day {day}", DAY_THEMES.get(day, ""), "—", "—", "—", "—", "—", "Route data pending"])

    rows.append(["TOTAL", "", t["total_distance_km"], t["total_co2_g"],
                 t["all_taxi_co2_g"], f"{t['co2_saved_pct']}%", "", ""])

    rows.extend([
        ["", "", "", "", "", "", "", ""],
        # Smart choices
        ["SMART TRANSPORT CHOICES", "", "", "", "", "", "", ""],
        ["Day 1:", "Metro from Pudong Airport (40km) instead of taxi — saved ~3,600g", "", "", "", "", "", ""],
        ["Day 2:", "Walking-first Old Town exploration — only 203g for the entire day", "", "", "", "", "", ""],
        ["Day 3:", "Single metro ride to Pudong, then 100% walking — lowest day (107g)", "", "", "", "", "", ""],
        ["Day 6:", "HSR to Suzhou (6g/km) instead of taxi (120g/km) — saved ~10kg", "", "", "", "", "", ""],
        ["Overall:", f"Taxi used for only {mode_totals.get('taxi', 0):.1f} km of {total_dist} km total ({mode_pcts.get('taxi', 0)}%)", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        # Emission factors
        ["EMISSION FACTORS (g CO2/km/person)", "", "", "", "", "", "", ""],
        ["Walking", "Metro", "Bus", "Taxi", "E-taxi", "HSR Train", "Maglev", ""],
        ["0", "29", "65", "120", "45", "6", "95", ""],
        ["—", "Shentong Metro", "Shanghai Bus Co.", "Avg petrol", "Shanghai grid", "China State Rail", "NDRC", ""],
        ["", "", "", "", "", "", "", ""],
        ["METHODOLOGY", "", "", "", "", "", "", ""],
        ["CO2 = distance_km x emission_factor. Shanghai-specific factors from 2024 published sources.", "", "", "", "", "", "", ""],
        [f"{len(co2.get('days', []))} of 6 days computed. See docs/sustainability-methodology.md for full methodology, limitations, and scoring criteria.", "", "", "", "", "", "", ""],
    ])

    ws.update(range_name="A1", values=rows, value_input_option="USER_ENTERED")

    # Formatting
    ws.format("A1", {"textFormat": {"bold": True, "fontSize": 16}})

    # Headline numbers - big and colored
    ws.merge_cells("A3:B3")
    ws.merge_cells("C3:D3")
    ws.merge_cells("E3:F3")
    ws.merge_cells("A4:B4")
    ws.merge_cells("C4:D4")
    ws.merge_cells("E4:F4")
    ws.format("A3:B3", {"textFormat": {"bold": True, "fontSize": 24},
                         "backgroundColor": {"red": 0.84, "green": 0.96, "blue": 0.84},
                         "horizontalAlignment": "CENTER"})
    ws.format("C3:D3", {"textFormat": {"bold": True, "fontSize": 24},
                         "backgroundColor": {"red": 0.78, "green": 0.93, "blue": 0.78},
                         "horizontalAlignment": "CENTER"})
    ws.format("E3:F3", {"textFormat": {"bold": True, "fontSize": 24},
                         "backgroundColor": {"red": 0.84, "green": 0.91, "blue": 0.96},
                         "horizontalAlignment": "CENTER"})
    ws.format("A4:F4", {"textFormat": {"fontSize": 10}, "horizontalAlignment": "CENTER"})

    # Section headers
    ws.format("A6", {"textFormat": {"bold": True, "fontSize": 12}})
    ws.format("A10", {"textFormat": {"bold": True, "fontSize": 12}})
    ws.format("A11:C11", {"textFormat": {"bold": True}})
    ws.format("A17", {"textFormat": {"bold": True, "fontSize": 12}})
    ws.format("A18:H18", {"textFormat": {"bold": True},
                           "backgroundColor": {"red": 0.94, "green": 0.94, "blue": 0.94}})

    # Smart choices
    smart_start = 18 + 8  # after daily rows + total + blank
    ws.format(f"A{smart_start}", {"textFormat": {"bold": True, "fontSize": 12}})

    # Emission factors - small gray
    ef_start = smart_start + 8
    ws.format(f"A{ef_start}:H{ef_start + 4}", {"textFormat": {"fontSize": 9,
              "foregroundColorStyle": {"rgbColor": {"red": 0.5, "green": 0.5, "blue": 0.5}}}})
    ws.format(f"A{ef_start}", {"textFormat": {"bold": True, "fontSize": 9}})

    # Methodology - italic
    meth_start = ef_start + 5
    ws.format(f"A{meth_start}", {"textFormat": {"bold": True, "fontSize": 10}})
    ws.format(f"A{meth_start + 1}:H{meth_start + 2}", {"textFormat": {"italic": True, "fontSize": 9}})

    ws.columns_auto_resize(0, 8)
    print("  Done")


# ============================================================
# TAB 4: PRE-TRIP CHECKLIST
# ============================================================

def build_checklist(sh):
    print("Building Pre-Trip Checklist...")
    try:
        ws = sh.worksheet("Pre-Trip Checklist")
        ws.clear()
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet(title="Pre-Trip Checklist", rows=55, cols=8)

    # Colors for categories
    cat_colors = {
        "APPS & PAYMENTS":          {"red": 0.89, "green": 0.95, "blue": 1.0},
        "TRANSPORT & CONNECTIVITY": {"red": 0.91, "green": 0.96, "blue": 0.91},
        "DOCUMENTS & SAFETY":       {"red": 1.0,  "green": 0.97, "blue": 0.88},
        "OFFLINE & MAPS":           {"red": 1.0,  "green": 0.95, "blue": 0.88},
        "SUSTAINABLE TRAVEL":       {"red": 0.88, "green": 0.95, "blue": 0.94},
        "GIS PROJECT":              {"red": 0.95, "green": 0.90, "blue": 0.96},
        "POST-TRIP":                {"red": 0.96, "green": 0.96, "blue": 0.96},
    }

    items = [
        # [done, when, priority, category, item, owner, notes]
        # APPS & PAYMENTS
        ["SECTION", "", "", "APPS & PAYMENTS", "", "", ""],
        [False, "2+ weeks", "critical", "Apps & Payments", "Download WeChat — install + verify phone number", "Both", "Need phone # for verification"],
        [False, "2+ weeks", "critical", "Apps & Payments", "Set up Alipay International — link foreign card", "Both", "Takes 2-3 days for identity verification"],
        [False, "1 week", "critical", "Apps & Payments", "Download Amap (高德地图)", "Both", "Primary navigation in China"],
        [False, "1 week", "recommended", "Apps & Payments", "Download Dianping (大众点评)", "Both", "Restaurant reviews — China's Yelp"],
        [False, "1 week", "recommended", "Apps & Payments", "Download Metro DaDuHui (大都会)", "Both", "QR code metro entry — no card needed"],
        [False, "1 week", "critical", "Apps & Payments", "Install + test VPN (ExpressVPN / Astrill)", "Both", "MUST test before entering China"],
        [False, "1 week", "recommended", "Apps & Payments", "Test Alipay with a small purchase", "Both", "Verify payment works before relying on it"],
        # TRANSPORT
        ["SECTION", "", "", "TRANSPORT & CONNECTIVITY", "", "", ""],
        [False, "2+ weeks", "critical", "Transport", "Book Suzhou HSR tickets (12306 or Trip.com)", "P1", "Specific dates + backup train times"],
        [False, "1 week", "critical", "Transport", "Get eSIM or China Unicom tourist SIM", "Both", "Data essential — many apps need internet"],
        [False, "on arrival", "recommended", "Transport", "Load Shanghai metro card or Alipay transit QR", "Both", "At airport convenience store or metro counter"],
        [False, "1 week", "recommended", "Transport", "Research airport → hotel route (metro)", "P1", "Metro Line 2 from PVG → transfer"],
        # DOCUMENTS
        ["SECTION", "", "", "DOCUMENTS & SAFETY", "", "", ""],
        [False, "2+ weeks", "critical", "Documents", "Passport — check validity > 6 months", "Both", ""],
        [False, "2+ weeks", "critical", "Documents", "China visa (check requirements for nationality)", "Both", "Some nationalities visa-free"],
        [False, "1 week", "critical", "Documents", "Hotel booking confirmation (EN + CN)", "P1", "Print + save digital copy"],
        [False, "2+ weeks", "critical", "Documents", "Travel insurance (covers China)", "Both", ""],
        [False, "day before", "recommended", "Documents", "Digital passport copy (phone + cloud)", "Both", "Photo of passport info page"],
        [False, "day before", "critical", "Documents", "Print hotel address in Chinese (large characters)", "Both", "Pocket card for taxi drivers"],
        [False, "day before", "recommended", "Documents", "Emergency contacts card (110 / 120 / 119 + embassy)", "Both", "Keep in wallet"],
        # OFFLINE
        ["SECTION", "", "", "OFFLINE & MAPS", "", "", ""],
        [False, "day before", "critical", "Offline", "Download Amap offline maps (Shanghai + Suzhou)", "Both", "In-app: My → Offline Maps"],
        [False, "day before", "recommended", "Offline", "Export QGIS PDF maps (Day 1-6)", "P2", "Run from QGIS print layout"],
        [False, "on arrival", "recommended", "Offline", "Pre-load web map on phone browser (WiFi + VPN)", "Both", "Service worker caches for offline"],
        [False, "day before", "recommended", "Offline", "Screenshot hotel address on phone home screen", "Both", "Fastest way to show taxi driver"],
        [False, "day before", "recommended", "Offline", "Download offline translation pack (Google Translate CN)", "Both", "Settings → Offline Translation"],
        # SUSTAINABLE
        ["SECTION", "", "", "SUSTAINABLE TRAVEL", "", "", ""],
        [False, "day before", "recommended", "Sustainable", "Pack reusable water bottle", "Both", "Shanghai tap water not drinkable — use refill stations"],
        [False, "day before", "recommended", "Sustainable", "Pack reusable shopping bag", "Both", "Plastic bags cost ¥ at shops"],
        [False, "1 week", "nice-to-have", "Sustainable", "Review heritage site etiquette guidelines", "P2", "Dress code for temples, no flash photography"],
        [False, "1 week", "nice-to-have", "Sustainable", "Research carbon offset for flight", "P2", "Know the number: ~250 kg CO2 one way"],
        # GIS PROJECT
        ["SECTION", "", "", "GIS PROJECT", "", "", ""],
        [False, "1 week", "critical", "GIS Project", "All POIs have day assignments (check data/poi/)", "Both", "Currently 19 of 50 assigned"],
        [False, "1 week", "critical", "GIS Project", "Route data complete for all 6 days", "P1", "Days 4-5 still pending"],
        [False, "1 week", "critical", "GIS Project", "Run CO2 calculator (python3 tools/co2-calculator.py)", "P2", "Outputs data/analysis/co2-summary.json"],
        [False, "day before", "critical", "GIS Project", "Web map deployed and tested on mobile", "P1", "Test on both phones"],
        [False, "day before", "recommended", "GIS Project", "Export final QGIS analysis maps", "P2", "Transit buffer + district choropleth"],
        [False, "day before", "recommended", "GIS Project", "Story map template ready", "P2", "web/story-template.html"],
        [False, "day before", "recommended", "GIS Project", "Update Google Sheet with final itinerary data", "Both", "This sheet!"],
        # POST-TRIP
        ["SECTION", "", "", "POST-TRIP", "", "", ""],
        [False, "post-trip", "recommended", "Post-trip", "Finalize story map with trip photos", "Both", "web/story-template.html"],
        [False, "post-trip", "recommended", "Post-trip", "Update actual vs. planned transport in Day tabs", "P2", "For sustainability comparison"],
        [False, "post-trip", "recommended", "Post-trip", "Write sustainability assessment summary", "P2", "SDG 11.2, 11.4, 12.b findings"],
        [False, "post-trip", "recommended", "Post-trip", "Run final CO2 calculation with actual modes", "P2", "Compare planned vs actual"],
    ]

    # Build rows
    header_rows = [
        ["PRE-TRIP CHECKLIST", "", "", "", "", "", ""],
        ['=COUNTIF(A4:A55,TRUE)&" of "&COUNTA(E4:E55)&" complete"', "", "", "", "", "", ""],
        ["DONE", "WHEN", "PRIORITY", "CATEGORY", "ITEM", "OWNER", "NOTES"],
    ]

    all_rows = header_rows.copy()
    section_row_indices = []

    for item in items:
        if item[0] == "SECTION":
            section_row_indices.append(len(all_rows))
            all_rows.append(["", "", "", item[3], "", "", ""])
        else:
            all_rows.append(item)

    ws.update(range_name="A1", values=all_rows, value_input_option="USER_ENTERED")

    # Formatting
    ws.merge_cells("A1:G1")
    ws.format("A1", {"textFormat": {"bold": True, "fontSize": 14}})
    ws.format("A2", {"textFormat": {"bold": True, "fontSize": 11}})
    ws.format("A3:G3", {"textFormat": {"bold": True},
                         "backgroundColor": {"red": 0.94, "green": 0.94, "blue": 0.94}})
    ws.freeze(rows=3)

    # Section headers
    requests = []
    sid = ws.id
    for idx in section_row_indices:
        row_num = idx + 1  # 1-indexed
        cat_name = all_rows[idx][3]
        color = cat_colors.get(cat_name, {"red": 0.95, "green": 0.95, "blue": 0.95})
        ws.merge_cells(f"A{row_num}:G{row_num}")
        ws.format(f"A{row_num}:G{row_num}", {
            "textFormat": {"bold": True, "fontSize": 10},
            "backgroundColor": color,
            "horizontalAlignment": "CENTER",
        })

    # Checkbox data validation on column A (non-section rows)
    checkbox_ranges = []
    for i, item in enumerate(items):
        if item[0] != "SECTION":
            row_idx = 3 + sum(1 for x in items[:items.index(item) + 1])  # approximate
    # Simpler: just apply to all of A4:A55
    requests.append({
        "setDataValidation": {
            "range": {"sheetId": sid, "startRowIndex": 3, "endRowIndex": len(all_rows),
                      "startColumnIndex": 0, "endColumnIndex": 1},
            "rule": {"condition": {"type": "BOOLEAN"}, "showCustomUi": True}
        }
    })

    # Owner dropdown
    requests.append({
        "setDataValidation": {
            "range": {"sheetId": sid, "startRowIndex": 3, "endRowIndex": len(all_rows),
                      "startColumnIndex": 5, "endColumnIndex": 6},
            "rule": {"condition": {"type": "ONE_OF_LIST",
                     "values": [{"userEnteredValue": v} for v in ["P1", "P2", "Both"]]},
                     "showCustomUi": True}
        }
    })

    # When dropdown
    requests.append({
        "setDataValidation": {
            "range": {"sheetId": sid, "startRowIndex": 3, "endRowIndex": len(all_rows),
                      "startColumnIndex": 1, "endColumnIndex": 2},
            "rule": {"condition": {"type": "ONE_OF_LIST",
                     "values": [{"userEnteredValue": v} for v in ["2+ weeks", "1 week", "day before", "at airport", "on arrival", "post-trip"]]},
                     "showCustomUi": True}
        }
    })

    sh.batch_update({"requests": requests})

    # Column widths
    col_widths = [50, 90, 80, 120, 300, 60, 250]
    width_requests = []
    for i, w in enumerate(col_widths):
        width_requests.append({
            "updateDimensionProperties": {
                "range": {"sheetId": sid, "dimension": "COLUMNS", "startIndex": i, "endIndex": i + 1},
                "properties": {"pixelSize": w}, "fields": "pixelSize"
            }
        })
    sh.batch_update({"requests": width_requests})

    print(f"  Done: {len([i for i in items if i[0] != 'SECTION'])} checklist items")


# ============================================================
# MAIN
# ============================================================

def main():
    print("Authenticating...")
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_url(SHEET_URL)

    pois = load_pois()
    co2 = load_co2()
    routes = load_routes()

    build_overview(sh, pois, co2, routes)
    print("  Waiting 65s for rate limit...")
    time.sleep(65)

    build_all_pois(sh, pois)
    print("  Waiting 65s for rate limit...")
    time.sleep(65)

    build_co2(sh, co2)
    print("  Waiting 65s for rate limit...")
    time.sleep(65)

    build_checklist(sh)

    print(f"\nAll 4 tabs rebuilt!")
    print(f"Sheet: {sh.url}")


if __name__ == "__main__":
    main()
