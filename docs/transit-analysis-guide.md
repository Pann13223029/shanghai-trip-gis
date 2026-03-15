# Transit Accessibility Analysis Guide

How to measure whether our trip's POIs are within walking distance of metro stations,
and what to do if some are not. This guide implements recommendation I-3 from the
expert panel using QGIS.

**Who this is for:** Person 2 performing the GIS analysis.
**Time required:** 30–45 minutes once the data is ready.
**QGIS skill level needed:** Beginner — every step is spelled out.

---

## Table of Contents

1. [Overview — What We Are Measuring and Why](#1-overview)
2. [Data Needed Before You Start](#2-data-needed)
3. [Step-by-Step QGIS Instructions](#3-step-by-step-qgis-instructions)
   - Step 1: Load metro stations
   - Step 2: Create 800m buffers
   - Step 3: Load all POI files
   - Step 4: Spatial join — POIs inside buffers
   - Step 5: Count the results
   - Step 6: Calculate the percentage
   - Step 7: Visualize — color by accessibility
   - Step 8: Export the result map
4. [How to Interpret Your Results](#4-how-to-interpret-results)
5. [Expected Output](#5-expected-output)

---

## 1. Overview

### What this analysis measures

This analysis answers one question:

> **"For each POI on our Shanghai itinerary, is there a metro station within 800 metres?"**

An 800m buffer around a station represents a comfortable, approximately 10-minute walk
for most people. If a POI falls inside that buffer, it is considered "transit-accessible."
If it falls outside all buffers, it requires a taxi, bus, or additional walking.

```
                   ┌─────────────────────────────────────┐
                   │                                     │
                   │         Metro Station               │
                   │              M                      │
                   │           .  |  .                   │
                   │        .     |     .   <-- 800m     │
                   │      .       |       .   buffer     │
                   │    .         |         .            │
                   │   .      ●  POI         .           │
                   │    .    (accessible!)  .            │
                   │      .               .              │
                   │        .           .                │
                   │          . . . . .                  │
                   │                          ● POI      │
                   │                     (NOT accessible │
                   │                      -- outside     │
                   │                         buffer)     │
                   └─────────────────────────────────────┘
```

### Why 800 metres?

The United Nations SDG indicator 11.2.1 ("Proportion of population that has convenient
access to public transport") uses 500m for bus stops and 1,000m for rail stations.
We use **800m** as our threshold — a practical middle ground that:

- Is stricter than the official 1,000m rail standard (our trips involve luggage and heat)
- Is more generous than the 500m bus standard (metro service is more reliable)
- Matches the transit accessibility scoring in the project's sustainability methodology
  (see `/docs/sustainability-methodology.md`, Transit Access dimension: score 2 = 400-800m,
  score 3 = <400m)

### The SDG 11.2 connection

**SDG Target 11.2** reads: "By 2030, provide access to safe, affordable, accessible and
sustainable transport systems for all, improving road safety, notably by expanding public
transport."

Indicator 11.2.1 was designed to measure city-wide transit access. We apply the same
spatial logic at the itinerary level: what proportion of the places we plan to visit
are genuinely reachable by public transit without a long walk?

A high percentage means our itinerary is transit-aligned. A low percentage signals that
we are planning a car-dependent trip, with higher carbon costs and higher reliance on taxis.

---

## 2. Data Needed

You need two datasets before opening QGIS.

### Dataset A — Shanghai Metro Station Locations

**File to create:** `data/routes/metro-stations-only.geojson`

This is a subset of the full metro GeoJSON containing only the station point features
(not the track lines). You can get it in two ways:

**Option 1 (recommended): Run the Overpass Turbo query**

Open `docs/overpass-queries.md` and go to **Query 2 — Metro Lines and Stations**.
Run the query in Overpass Turbo. After exporting, you will have a GeoJSON with both
station nodes and track lines mixed together.

To get stations only, use this focused query instead of the full Query 2:

```
/*
  Shanghai Metro Stations Only (no track lines)
  Returns only the station point nodes — faster to work with in QGIS
  for buffer analysis.
*/

[out:json][timeout:60];
(
  node["station"="subway"](30.7,120.8,31.5,121.9);
);

out body;
>;
out skel qt;
```

Save the export as: `data/routes/metro-stations-only.geojson`

Expected result: 400–550 point features (one per physical station, not per entrance).

**Option 2: Use the existing metro.geojson**

If `data/routes/metro.geojson` already exists in the project, you can load it in QGIS
and filter for the station nodes. See Step 1 below for how to handle this.

### Dataset B — Project POI Files

These already exist in the project. You will use all of them:

```
data/poi/
├── accommodation.geojson    (hotels)
├── cultural.geojson         (temples, museums, galleries)
├── food.geojson             (restaurants, cafes)
├── landmarks.geojson        (major sights, The Bund, etc.)
├── nature.geojson           (parks, gardens)
├── shopping.geojson         (malls, markets)
├── suzhou.geojson           (Day 6 Suzhou POIs)
└── transport.geojson        (airports, train stations)
```

Note: `transport.geojson` contains metro stations and airports that are themselves transit
nodes — they will trivially be inside buffers. You may choose to exclude this layer from
the analysis or keep it in. Either is defensible; just document your choice.

---

## 3. Step-by-Step QGIS Instructions

### Before you begin — Project Setup

```
Step 0a: Open QGIS

Step 0b: Add an OpenStreetMap base map
         Browser Panel → XYZ Tiles → OpenStreetMap (double-click)

Step 0c: Verify coordinates
         Zoom to Shanghai (121.47, 31.23)
         Check the bottom status bar — it should show EPSG:4326
         If it shows a different CRS, go to Project → Properties → CRS
         and set it to EPSG:4326 (WGS 84)

Step 0d: Save the project now
         Project → Save As → qgis/transit-analysis.qgz
```

---

### Step 1: Load Metro Stations into QGIS

```
Action: Menu → Layer → Add Layer → Add Vector Layer...

┌─ Add Vector Layer ────────────────────────────────┐
│                                                   │
│  Source Type:  ● File                             │
│                                                   │
│  Source:                                          │
│  ┌─────────────────────────────────────┐          │
│  │  .../data/routes/metro-stations-... │ [Browse] │
│  └─────────────────────────────────────┘          │
│                                                   │
│                           [Add]  [Close]          │
└───────────────────────────────────────────────────┘

Navigate to: data/routes/metro-stations-only.geojson
Click Add.
```

You should see hundreds of small dots scattered across Shanghai.

**Verify the data loaded correctly:**

```
1. Right-click the layer → Zoom to Layer
   You should see points covering Shanghai's urban core
   and spreading outward along metro lines.

2. Click the Identify tool (i icon in toolbar)
   Click one of the dots.
   The Identify Results panel should show tags like:
     name     = "人民广场"
     name:en  = "People's Square"
     station  = "subway"
     line     = "1;2;8"

3. Expected pattern:

   ┌────────────────────────────────────────────┐
   │                  ·  ·                      │
   │      · · · · · ·   · · · · ·               │
   │    ·      ·  ·  ·  ·   ·   ·  ·            │
   │   ·        · · · · · · · ·  · ·            │
   │  ·     · · · · · ·   · · · · ·             │
   │   · · · · ·   · · · · · · · ·              │
   │    · ·     · · · · · · ·   · ·             │
   │      · · · · ·   · · ·       ·             │
   │                 · ·                        │
   │   (dots = metro stations,                  │
   │    spread along 20 lines)                  │
   └────────────────────────────────────────────┘

If you see fewer than ~100 dots, or they are clustered in one area only,
the data may be incomplete. Re-run the Overpass query.
```

---

### Step 2: Create 800m Buffers Around All Stations

This is the core spatial operation. It draws a circle of radius 800m around every
metro station simultaneously.

```
Action: Menu → Vector → Geoprocessing Tools → Buffer...

┌─ Buffer ──────────────────────────────────────────────────────┐
│                                                               │
│  Input layer:      [ metro-stations-only          ▼]         │
│                                                               │
│  Distance:         [ 800   ]                                  │
│  Units:            [ meters                       ▼]         │
│                                                               │
│  Segments:         [ 36    ]  (smoothness — 36 is fine)      │
│                                                               │
│  Dissolve result:  [ checked / true ]  <-- IMPORTANT         │
│                      (merges overlapping circles into one     │
│                       continuous "coverage area" shape)       │
│                                                               │
│  Output:           [ Save to file... ]                        │
│  Save as:          .../data/routes/metro-buffers-800m.geojson │
│                                                               │
│                                              [Run]            │
└───────────────────────────────────────────────────────────────┘
```

**Why "Dissolve result" matters:**

```
WITHOUT dissolve:                    WITH dissolve:
Each station gets its own circle.    Overlapping circles merge.
                                     You get one solid shape showing
  ( ) ( ) ( ) ( )                    total metro coverage area.
   (   (   )   )
    (overlap)                         /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\
                                     /   continuous      \
                                    |   coverage area     |
                                     \___________________/

Use dissolve=true for the "% POIs covered" calculation.
Use dissolve=false if you want to know WHICH station is closest.
For this analysis, use dissolve=true.
```

Click **Run**. QGIS will process for a few seconds. A new layer named "Buffered"
(or your saved filename) appears in the Layers Panel.

**Verify the buffer looks right:**

```
What you should see:

┌──────────────────────────────────────────────────────────────┐
│                                                              │
│        Metro coverage area (shaded):                         │
│                                                              │
│     ╔══════════════════════════════════════╗                 │
│    ╔╣  .  .  .  .  .  .  .  .  .  .  .   ╠╗                │
│   ╔╣║  Continuous shaded region covering  ║╣╗               │
│   ║╣║  the urban core of Shanghai         ║╣║               │
│   ╚╣║                                     ║╣╝               │
│    ╚╣  .  .  .  .  .  .  .  .  .  .  .   ╣╝                │
│     ╚══════════════════════════════════════╝                 │
│                                                              │
│   Note: Outer suburbs may show isolated circles where        │
│   stations are farther apart. The city centre should         │
│   appear as one large connected coverage zone.               │
│                                                              │
└──────────────────────────────────────────────────────────────┘

If you see a tiny speck or nothing at all:
  --> Units are wrong. Buffer used degrees, not meters.
  --> Re-run with Units: meters explicitly selected.
  --> Also check: Project → Properties → CRS is EPSG:4326 (not projected).
      If using EPSG:4326, QGIS may need you to use a projected CRS instead.
      See the CRS note at the end of this step.
```

**CRS note — if the buffer looks tiny:**

QGIS measures buffers in the layer's native units. For EPSG:4326 (degrees), 800 degrees
is absurd and 800 metres needs conversion. The easiest fix:

```
Option A: Re-project before buffering
  Right-click metro-stations layer → Export → Save Features As
  CRS: EPSG:32651 (WGS 84 / UTM zone 51N — correct zone for Shanghai)
  Save as: metro-stations-utm.geojson

  Then run Buffer on the UTM version with Distance: 800, Units: meters.
  The output buffer will also be in UTM — that is fine for analysis.
  QGIS will reproject it on-the-fly when displaying alongside WGS84 layers.

Option B: Use QGIS "Buffer (variable distance)" in the Processing Toolbox
  Search: Processing Toolbox → search "buffer"
  Use "Buffer" under Vector geometry
  In the Distance field, click the small epsilon (ε) button → edit
  Enter: 800 / 111000  (converts 800m to approximate degrees)
  This is a rough approximation; Option A is more accurate.
```

---

### Step 3: Load All POI Files

Load each POI file from `data/poi/` into QGIS.

```
Action: Menu → Layer → Add Layer → Add Vector Layer...
Repeat for each file, or drag-and-drop multiple files at once.

Files to load:
  data/poi/accommodation.geojson
  data/poi/cultural.geojson
  data/poi/food.geojson
  data/poi/landmarks.geojson
  data/poi/nature.geojson
  data/poi/shopping.geojson
  data/poi/suzhou.geojson
  data/poi/transport.geojson
```

After loading, your Layers Panel should look like:

```
┌─ Layers ──────────────────────────────────────────┐
│  ☑ transport                                      │
│  ☑ suzhou                                         │
│  ☑ shopping                                       │
│  ☑ nature                                         │
│  ☑ landmarks                                      │
│  ☑ food                                           │
│  ☑ cultural                                       │
│  ☑ accommodation                                  │
│  ☑ metro-buffers-800m       <-- the buffer layer  │
│  ☑ metro-stations-only      <-- the stations      │
│  ☑ OpenStreetMap            <-- base map          │
└───────────────────────────────────────────────────┘
```

**Tip:** Drag the buffer layer to just above OpenStreetMap so it does not cover your POI dots.
Set the buffer layer's opacity to 30-40% so you can see the base map through it:

```
Right-click metro-buffers-800m → Properties → Symbology
  Fill color: light blue  (#85c1e9)
  Opacity: 30%
  Stroke: none (or thin blue)
→ Apply → OK
```

This gives a visual where blue shading = "metro coverage zone."

---

### Step 4: Spatial Join — Count POIs Inside Buffers

This is the key analysis step. QGIS will check each POI and tag it: "inside buffer" or
"outside buffer."

```
Action: Menu → Vector → Data Management Tools → Join Attributes by Location...

┌─ Join Attributes by Location ──────────────────────────────────────────┐
│                                                                        │
│  Join to features in:   [ landmarks              ▼]                   │
│   (the layer receiving the new attribute)                              │
│                                                                        │
│  Where the features:    [ intersect              ▼]                   │
│   (spatial relationship — "intersect" means "are inside or touch")    │
│                                                                        │
│  By comparing to:       [ metro-buffers-800m     ▼]                   │
│   (the reference layer)                                                │
│                                                                        │
│  Fields to add:         [ ✓ All fields ]  or leave default            │
│                                                                        │
│  Join type:             [ ● Create separate feature for each          │
│                            matching feature (one-to-many)  ]          │
│                          OR                                            │
│                         [ ● Take attributes of the first              │
│                            matching feature only           ]  <-- use │
│                                                                        │
│  Joined layer:          [ Save to file... ]                           │
│  Save as:   .../data/poi/landmarks-with-transit.geojson               │
│                                                                        │
│                                                   [Run]               │
└────────────────────────────────────────────────────────────────────────┘
```

**Repeat this for every POI layer** (cultural, food, nature, shopping, accommodation,
suzhou, transport). Save each with a `-with-transit` suffix:

```
landmarks   → landmarks-with-transit.geojson
cultural    → cultural-with-transit.geojson
food        → food-with-transit.geojson
nature      → nature-with-transit.geojson
shopping    → shopping-with-transit.geojson
accommodation → accommodation-with-transit.geojson
suzhou      → suzhou-with-transit.geojson
transport   → transport-with-transit.geojson
```

**What the join does — visualised:**

```
Before join:                         After join:

POI layer:                           POI layer (enriched):
  ● The Bund                           ● The Bund
      name: "The Bund"                     name: "The Bund"
      category: landmark                   category: landmark
      day: 1                               day: 1
                                           metro_buffer_id: 47  <-- NEW
                                           (non-null = inside a buffer)

  ● Chenshan Botanical Garden          ● Chenshan Botanical Garden
      name: "Chenshan..."                  name: "Chenshan..."
      category: nature                     category: nature
      day: 5                               day: 5
                                           metro_buffer_id: null  <-- NEW
                                           (null = outside all buffers)
```

POIs where the join field is **non-null** = within 800m of a metro station.
POIs where the join field is **null** = NOT within 800m of any metro station.

---

### Step 5: Count the Results

After running the spatial join, open the Attribute Table to count:

```
Action: Right-click landmarks-with-transit → Open Attribute Table

┌─ Attribute Table: landmarks-with-transit ──────────────────────────────┐
│  [Filter expressions]                                           56 / 56 │
│                                                                        │
│  id            name_en               day  metro_buffer_id              │
│  landmark-001  The Bund              1    47          ← inside buffer  │
│  landmark-002  Yu Garden             1    23          ← inside buffer  │
│  landmark-003  Chenshan Bot. Garden  5    (null)      ← OUTSIDE        │
│  landmark-004  Oriental Pearl Tower  3    61          ← inside buffer  │
│  ...                                                                   │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

**To count "inside buffer" vs. "outside buffer" quickly:**

Use the Field Calculator or Filter Bar:

```
Step 1: In the Attribute Table, click the filter icon (funnel) at the bottom.

Step 2: Type this expression to select only "outside buffer" features:
          "metro_buffer_id" IS NULL
        or (if QGIS used a field name from the buffer layer, try):
          "fid_2" IS NULL

Step 3: Click Select Features.
        The status bar at the top right shows:
          "Selected: 3 / 56"
        This means 3 out of 56 landmarks are NOT transit-accessible.

Step 4: Repeat for each layer.

Step 5: Record your counts in a table like this:

┌────────────────────┬────────┬───────────┬─────────┬──────────────┐
│ Layer              │ Total  │ Inside    │ Outside │ % Inside     │
│                    │  POIs  │  Buffer   │ Buffer  │  (coverage)  │
├────────────────────┼────────┼───────────┼─────────┼──────────────┤
│ landmarks          │        │           │         │              │
│ cultural           │        │           │         │              │
│ food               │        │           │         │              │
│ nature             │        │           │         │              │
│ shopping           │        │           │         │              │
│ accommodation      │        │           │         │              │
│ suzhou             │        │           │         │              │
│ transport          │        │           │         │              │
├────────────────────┼────────┼───────────┼─────────┼──────────────┤
│ TOTAL (all layers) │        │           │         │              │
└────────────────────┴────────┴───────────┴─────────┴──────────────┘
```

---

### Step 6: Calculate the Percentage

Once you have the counts, the calculation is straightforward:

```
Formula:
  % Transit-Accessible = (POIs inside buffer / Total POIs) × 100

Example:
  If you counted 48 POIs inside buffers out of 56 total:
    48 / 56 × 100 = 85.7%

  This means 85.7% of our POIs are within 800m of a metro station.

Record separately:
  - Overall % (all layers combined)
  - % per category (landmarks only, food only, etc.)
  - % per day (Day 1 only, Day 2 only, etc.)

The per-day breakdown is most useful for planning:
  If Day 5 has 60% coverage but Day 2 has 95%, it tells you
  Day 5 needs the most taxi/bus planning.
```

**Optional: Day-by-day breakdown**

In the Attribute Table, filter by `"day" = 1`, then count inside/outside.
Repeat for each day. This gives you a transit score per day.

```
Day-by-day target:

  Day 1 (Arrival/Bund)       → expect high coverage (city centre)
  Day 2 (French Concession)  → expect high coverage
  Day 3 (Pudong/Lujiazui)    → expect high coverage (Line 2)
  Day 4 (Jing'an/Museums)    → expect high coverage
  Day 5 (Parks/outer areas)  → may be lower (some parks are remote)
  Day 6 (Suzhou)             → Suzhou has its own metro — check separately
```

---

### Step 7: Visualize — Color POIs by Transit Accessibility

Create a map where POIs are color-coded by whether they are transit-accessible.

```
Action: Merge all *-with-transit layers first:
  Menu → Processing → Toolbox → search "Merge vector layers"

  ┌─ Merge Vector Layers ────────────────────────────┐
  │                                                  │
  │  Input layers:  [ all *-with-transit files ]     │
  │                 landmarks-with-transit           │
  │                 cultural-with-transit            │
  │                 food-with-transit                │
  │                 ... etc.                         │
  │                                                  │
  │  Output:        [ all-pois-with-transit.geojson ]│
  │                                                  │
  │                                       [Run]      │
  └──────────────────────────────────────────────────┘
```

Now apply a Rule-Based style to color by transit access:

```
Right-click all-pois-with-transit → Properties → Symbology

Change dropdown from "Single Symbol" to "Rule-based"

┌─ Symbology: Rule-based ───────────────────────────────────────────┐
│                                                                   │
│  [+] Add rule button (bottom left)                                │
│                                                                   │
│  Rule 1:                                                          │
│    Label:  "Within 800m of metro"                                 │
│    Filter: "metro_buffer_id" IS NOT NULL                          │
│    Symbol: ● circle, color #27ae60 (GREEN), size 8               │
│                                                                   │
│  Rule 2:                                                          │
│    Label:  "NOT transit-accessible"                               │
│    Filter: "metro_buffer_id" IS NULL                              │
│    Symbol: ● circle, color #e74c3c (RED), size 8                 │
│    (optionally: add a larger outline/halo to make them stand out) │
│                                                                   │
│                                         [Apply]  [OK]            │
└───────────────────────────────────────────────────────────────────┘
```

The resulting map should look like:

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│         Transit Accessibility Map                                │
│                                                                  │
│   ████████████████████████████                                   │
│  ██  ●green ●green   ●green  ███                                 │
│  ██    ●green ●green          ██                                 │
│  ██████████████████████████████                                  │
│     ████████████████████████                                     │
│       ██  ●green ●green  ██                                      │
│       ██    ●green       ██                                      │
│       ████████████████████                                       │
│                                                                  │
│                        ●red   ← outside metro coverage           │
│                    ●red       ← needs taxi/bus                   │
│                                                                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                                 │
│  LEGEND                                                          │
│  ● green  = within 800m of metro (transit-accessible)           │
│  ● red    = outside 800m (needs taxi or bus)                     │
│  ████     = 800m metro coverage area                             │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Add labels for the red (non-accessible) POIs so they are easy to identify:**

```
Right-click all-pois-with-transit → Properties → Labels
  Label with:   name_en
  Filter:       "metro_buffer_id" IS NULL   (label only the red ones)
  Font size:    8pt
  Buffer:       white halo, 1mm  (makes text readable over the map)
→ Apply → OK
```

---

### Step 8: Export the Result Map

```
Step 1: Set up the map view
  - Zoom to show all of Shanghai with POIs visible
  - Make sure the buffer layer, the colored POI layer, and OSM base map
    are all visible and in the right draw order

Step 2: Create a Print Layout
  Menu → Project → New Print Layout
  Name: "Transit Accessibility Analysis"

Step 3: Add layout elements

  a) Map frame (the map itself):
     Click Add Map tool → draw a large rectangle on the page
     Item Properties → Set to map canvas extent

  b) Title:
     Add Label → draw at top
     Text: "Shanghai Trip — Transit Accessibility Analysis"
     Subtitle (smaller): "% of POIs within 800m of a metro station"

  c) Legend:
     Add Legend → draw in corner
     Remove unwanted entries — keep only:
       ● Within 800m of metro  (green)
       ● NOT transit-accessible (red)
       ████ 800m coverage area (blue)

  d) Scale bar:
     Add Scale Bar → draw at bottom
     Units: meters, style: "Single Box"

  e) Statistics box (add as a text label):
     "Analysis result: X% of POIs are transit-accessible (N/N total)"
     Use your calculated figures from Steps 5-6.

  f) North arrow:
     Add North Arrow → draw in corner

Step 4: Layout should look roughly like:

  ┌────────────────────────────────────────────────────┐
  │                                                    │
  │   Shanghai Trip — Transit Accessibility Analysis   │
  │   % of POIs within 800m of a metro station         │
  │                                                    │
  │   ┌──────────────────────────────────────────┐     │
  │   │                                          │     │
  │   │         [MAP — colored POIs             │     │
  │   │          overlaid on coverage area]      │     │
  │   │                                          │     │
  │   └──────────────────────────────────────────┘     │
  │                                                    │
  │   LEGEND              ├──500m──┤                   │
  │   ● Within 800m                  ^                 │
  │   ● NOT accessible               N                 │
  │   ██ Coverage area                                 │
  │                                                    │
  │   Result: 87% of POIs are transit-accessible       │
  │   (42 of 48 total trip POIs)                       │
  │   SDG 11.2 analysis | Shanghai Trip 2026            │
  │                                                    │
  └────────────────────────────────────────────────────┘

Step 5: Export as PNG (for reports/slides) and PDF (for printing)
  Menu → Layout → Export as Image → save as transit-accessibility-map.png
  Menu → Layout → Export as PDF  → save as transit-accessibility-map.pdf

  Save to: qgis/outputs/  (create this folder if it does not exist)
```

---

## 4. How to Interpret Results

### What the percentage means

```
┌────────────────────────────────────────────────────────────────────┐
│  Coverage %    Interpretation                  Action needed       │
├────────────────┼───────────────────────────────┼───────────────────┤
│  90% or above  │ Excellent — the itinerary      │ None required.    │
│                │ is highly transit-aligned.     │ Document and     │
│                │ Consistent with SDG 11.2       │ celebrate.       │
│                │ goals for urban areas.         │                  │
├────────────────┼───────────────────────────────┼───────────────────┤
│  75% – 89%     │ Good — most POIs are           │ Review the red   │
│                │ accessible. A few outliers     │ POIs and plan    │
│                │ need alternative transport.    │ taxi/bus for     │
│                │                               │ those days.      │
├────────────────┼───────────────────────────────┼───────────────────┤
│  50% – 74%     │ Mixed — significant portion    │ Consider         │
│                │ of the trip relies on taxis.   │ re-routing some  │
│                │ Carbon cost is higher.         │ POIs. Group non- │
│                │                               │ accessible POIs  │
│                │                               │ on same day.     │
├────────────────┼───────────────────────────────┼───────────────────┤
│  Below 50%     │ Poor transit alignment —       │ Significant re-  │
│                │ the trip is more car-          │ planning needed. │
│                │ dependent than ideal.          │ Many POIs may    │
│                │                               │ need reassigning │
│                │                               │ or dropping.     │
└────────────────┴───────────────────────────────┴───────────────────┘
```

### What to do if many POIs lack transit access

**Option A: Reassign to different days to cluster non-accessible POIs**

```
Current plan:                         Better plan:
  Day 4: ●accessible ●accessible        Day 4: ●accessible ●accessible
         ●accessible ●RED               Day 5: ●RED ●RED ●RED
         ●accessible                    (one taxi day instead of
  Day 5: ●accessible ●RED               scattered taxi trips each day)
         ●RED ●accessible
```

Group all "red" POIs into one day. Arrange a single taxi circuit for that day.
This minimises taxi use without dropping POIs.

**Option B: Find the nearest metro station and walk**

For POIs just outside the 800m buffer, check the actual distance. If a POI is
at 850m–1,000m from a station, it may still be acceptable with a slightly longer walk.

```
In QGIS: use the Measure tool (ruler icon) to check straight-line distance
  from the POI to the nearest station.

Straight-line 850m → actual walk ~1,100m → ~14 minutes
  → still reasonable in good weather

Straight-line 1,500m → actual walk ~1,950m → ~25 minutes
  → probably needs a taxi
```

**Option C: Use Didi (ride-hail) for the "last mile"**

For POIs in areas with poor metro access, note them in the itinerary as
"Didi from [nearest station]." This maintains metro use for the long haul
and adds a short taxi leg only where necessary.

**Option D: Reassess whether the POI should stay in the itinerary**

If a POI is remote, has no realistic transit access, and is not a high-priority
stop, consider removing it. This is a sustainability trade-off worth documenting.

### Reference to methodology

For the scoring scale (0–3) used in each POI's sustainability scorecard, see
`docs/sustainability-methodology.md` under "Sustainability Scorecard" →
"Transit access" dimension. This analysis provides the spatial evidence needed
to assign accurate transit access scores to all POIs at once.

---

## 5. Expected Output

By the end of this analysis you should have produced three things:

### Output 1 — The statistic

A single sentence suitable for the report and presentation:

```
"X% of our POIs are within 800m of a metro station (N of N total POIs
analysed), measured against the SDG 11.2.1 transit access threshold."
```

Example:
```
"87% of our POIs are within 800m of a metro station (42 of 48 total POIs
analysed), measured against the SDG 11.2.1 transit access threshold."
```

### Output 2 — The map

A print-quality map (PNG + PDF) saved to `qgis/outputs/` showing:

```
  ┌───────────────────────────────────────────────────────┐
  │                                                       │
  │   ● green dots = transit-accessible POIs             │
  │   ● red dots   = POIs needing taxi/bus               │
  │   blue shading = 800m metro coverage zone            │
  │   base map     = OpenStreetMap                       │
  │   statistics box showing overall % coverage          │
  │                                                       │
  └───────────────────────────────────────────────────────┘
```

### Output 3 — The list of non-accessible POIs

Export the red POIs (those with `metro_buffer_id IS NULL`) as a separate file
and as a simple text list:

```
Action: In Attribute Table → filter "metro_buffer_id" IS NULL
        → Select All Filtered
        → Right-click layer → Export → Save Selected Features As
        Save as: data/poi/non-transit-pois.geojson

Also write out a plain-text list:
  POIs NOT within 800m of a metro station:
  --------------------------------------------------------
  1. [name_en]  — Day [day]  — Category: [category]
  2. ...
  --------------------------------------------------------
  Total: N POIs need taxi or bus alternative transport.
  Estimated additional CO2 vs. metro-only:
    N × avg 5km taxi ride × 120g/km = ~Xg CO2 extra per person
    (use emission factors from sustainability-methodology.md)
```

This list becomes the action item for transport planning:
each non-accessible POI needs a note in the day-by-day itinerary
specifying which transport mode will be used instead.

---

## Quick Summary — The Eight Steps

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  TRANSIT ACCESSIBILITY ANALYSIS — WORKFLOW OVERVIEW                 │
│                                                                     │
│  [1] Load metro stations      (data/routes/metro-stations-only)     │
│          │                                                          │
│          ▼                                                          │
│  [2] Create 800m buffers      (Vector → Geoprocessing → Buffer)     │
│          │                                                          │
│          ▼                                                          │
│  [3] Load all POI layers      (data/poi/*.geojson)                  │
│          │                                                          │
│          ▼                                                          │
│  [4] Spatial join             (Vector → Data Management →           │
│          │                     Join Attributes by Location)         │
│          ▼                                                          │
│  [5] Count inside / outside   (Attribute Table → filter IS NULL)    │
│          │                                                          │
│          ▼                                                          │
│  [6] Calculate %              (inside ÷ total × 100)               │
│          │                                                          │
│          ▼                                                          │
│  [7] Visualize                (Rule-based: green / red)             │
│          │                                                          │
│          ▼                                                          │
│  [8] Export map + stats       (Print Layout → PNG + PDF)            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

*Analysis framework: SDG indicator 11.2.1 (Sustainable Development Goals, UN 2015)*
*Threshold: 800m walking distance to rail transit (SDG 11.2 rail standard = 1,000m; bus = 500m)*
*For emission factor context used alongside this analysis, see `docs/sustainability-methodology.md`*
*For Overpass Turbo queries to download metro station data, see `docs/overpass-queries.md` Query 2*
