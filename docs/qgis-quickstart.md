# QGIS Quickstart Guide

A visual, step-by-step guide to get you productive in QGIS for this project. No prior experience needed.

---

## 1. Install & First Launch

Download QGIS LTR (Long Term Release) from [qgis.org/download](https://qgis.org/en/site/forusers/download.html).

When you first open QGIS, you'll see this layout:

```
┌──────────────────────────────────────────────────────────────────┐
│  File   Edit   View   Layer   Processing   Help                  │
├──────────────────────────────────────────────────────────────────┤
│ [toolbar icons: save, undo, zoom, pan, measure, select, ...]    │
├────────────┬─────────────────────────────────────────────────────┤
│            │                                                     │
│  BROWSER   │                                                     │
│  PANEL     │                                                     │
│            │              MAP CANVAS                              │
│  (files &  │              (this is where your map appears)        │
│  databases)│                                                     │
│            │                                                     │
├────────────┤                                                     │
│            │                                                     │
│  LAYERS    │                                                     │
│  PANEL     │                                                     │
│            │                                                     │
│  (your     │                                                     │
│  data      │                                                     │
│  layers)   │                                                     │
│            │                                                     │
├────────────┴─────────────────────────────────────────────────────┤
│  Coordinate: 121.4737, 31.2304    Scale: 1:50000    EPSG:4326   │
└──────────────────────────────────────────────────────────────────┘
```

**Key panels:**
- **Browser Panel** (top-left) — navigate your computer's files
- **Layers Panel** (bottom-left) — shows what's on the map, toggle visibility
- **Map Canvas** (center) — the map itself
- **Status Bar** (bottom) — shows coordinates, scale, and CRS

---

## 2. Add a Base Map (OpenStreetMap)

You need a background map so your POIs have geographic context.

```
Step 1:  In the Browser Panel, find "XYZ Tiles"
         ┌─ Browser ──────────────┐
         │  ▶ Favorites           │
         │  ▶ Home                │
         │  ▶ GeoPackage          │
         │  ▼ XYZ Tiles           │
         │     └── OpenStreetMap  │  <── double-click this
         └────────────────────────┘

Step 2:  Double-click "OpenStreetMap"
         A world map appears in the Map Canvas!

Step 3:  Zoom to Shanghai:
         - Use scroll wheel to zoom
         - Click and drag to pan
         - Or type in the coordinate bar at the bottom:
           121.47, 31.23  then press Enter
```

Your Layers Panel should now look like:

```
┌─ Layers ─────────────────┐
│  ☑ OpenStreetMap          │
└──────────────────────────┘
```

---

## 3. Load Your GeoJSON Files

Now add the project's POI data on top of the base map.

```
Step 1:  Menu → Layer → Add Layer → Add Vector Layer...

         ┌─ Add Vector Layer ──────────────────────────┐
         │                                              │
         │  Source Type:  ● File                        │
         │                                              │
         │  Source:                                      │
         │  ┌────────────────────────────────┐          │
         │  │ /path/to/data/poi/landmarks... │ [Browse] │
         │  └────────────────────────────────┘          │
         │                                              │
         │              [Add]  [Close]                   │
         └──────────────────────────────────────────────┘

Step 2:  Click [Browse], navigate to the project folder:
         shanghai-trip-gis/data/poi/landmarks.geojson

Step 3:  Click [Add]. Dots appear on the map!

Step 4:  Repeat for all POI files:
         - food.geojson
         - shopping.geojson
         - cultural.geojson
         - nature.geojson
         - transport.geojson
         - accommodation.geojson
         - suzhou.geojson
```

**Shortcut:** You can also drag-and-drop `.geojson` files from your file explorer directly into the Layers Panel.

Your Layers Panel should now look like:

```
┌─ Layers ──────────────────┐
│  ☑ suzhou                  │  ← layers on top draw over layers below
│  ☑ accommodation           │
│  ☑ transport               │
│  ☑ nature                  │
│  ☑ cultural                │
│  ☑ shopping                │
│  ☑ food                    │
│  ☑ landmarks               │
│  ☑ OpenStreetMap            │  ← base map always at the bottom
└───────────────────────────┘

Tip: Click the ☑ checkbox to toggle a layer on/off
     Drag layers up/down to change drawing order
```

---

## 4. Navigate the Map

```
┌──────────────────────────────────────┐
│                                      │
│  Mouse Controls:                     │
│                                      │
│    Scroll wheel     = Zoom in/out    │
│    Click + drag     = Pan            │
│    Right-click drag = Pan (alt)      │
│                                      │
│  Keyboard:                           │
│                                      │
│    +  /  -          = Zoom in/out    │
│    Arrow keys       = Pan            │
│    Ctrl + Shift + F = Zoom to all    │
│                                      │
│  Toolbar:                            │
│                                      │
│    🔍+ = Zoom in    🔍- = Zoom out   │
│    🖐  = Pan         🔍🌐 = Zoom all  │
│                                      │
└──────────────────────────────────────┘
```

**Zoom to your data:** Right-click any layer in the Layers Panel → "Zoom to Layer"

---

## 5. Identify a Feature (Click to See Details)

```
Step 1:  Click the "Identify" tool in the toolbar
         (it looks like an arrow with an "i")

         Toolbar:  ... [🖐 Pan] [ℹ️ Identify] [📏 Measure] ...

Step 2:  Click on any POI dot on the map

Step 3:  An "Identify Results" panel appears:

         ┌─ Identify Results ──────────────────┐
         │                                      │
         │  landmarks - Feature 1               │
         │                                      │
         │  id             : landmark-001       │
         │  name_en        : The Bund           │
         │  name_cn        : 外滩               │
         │  category       : landmark           │
         │  day            : null               │
         │  description    : Iconic 1.5km...    │
         │  priority       : must-visit         │
         │  est_duration   : 60                 │
         │  est_cost_cny   : 0                  │
         │  ...                                 │
         │                                      │
         └──────────────────────────────────────┘
```

This is how you verify your data — click a POI and check all the properties are correct.

---

## 6. Style Layers by Category (Color Your POIs)

By default, all layers use random colors. Let's match our project's color scheme.

```
Step 1:  Right-click a layer (e.g., "landmarks") → Properties

Step 2:  Click "Symbology" tab on the left

         ┌─ Layer Properties ──────────────────────────────┐
         │                                                  │
         │  [ℹ Info]  [🔵 Symbology]  [📝 Labels]  [...]   │
         │                                                  │
         │  Symbol type: ● Simple Marker                    │
         │                                                  │
         │  ┌──────────────────────────┐                    │
         │  │  Color:    [■ red     ▼] │ ← click to change │
         │  │  Size:     [  8       ▼] │                    │
         │  │  Shape:    [● circle  ▼] │                    │
         │  └──────────────────────────┘                    │
         │                                                  │
         │                      [Apply]  [OK]               │
         └──────────────────────────────────────────────────┘

Step 3:  Set colors to match our project scheme:
```

Use these colors for each layer:

```
  landmarks       → ■ #e74c3c  (red)
  food            → ■ #e67e22  (orange)
  shopping        → ■ #9b59b6  (purple)
  cultural        → ■ #3498db  (blue)
  nature          → ■ #27ae60  (green)
  transport       → ■ #7f8c8d  (gray)
  accommodation   → ■ #f1c40f  (yellow)
  suzhou          → ■ #1abc9c  (teal)
```

---

## 7. Color POIs by Day (Itinerary Check)

This is the key analysis view — see if same-day POIs are geographically grouped.

```
Step 1:  Merge all POI layers into a temporary view:
         Menu → Processing → Toolbox → search "Merge vector layers"
         Add all POI layers → Run → creates a merged layer

Step 2:  Right-click merged layer → Properties → Symbology

Step 3:  Change the dropdown at the top from "Single Symbol" to "Categorized"

         ┌─ Symbology ────────────────────────────────────┐
         │                                                 │
         │  [ Categorized          ▼]  ← change this      │
         │                                                 │
         │  Column:  [ day         ▼]  ← select "day"     │
         │                                                 │
         │  [Classify]  ← click this button                │
         │                                                 │
         │  ┌─────────────────────────────────┐            │
         │  │  Symbol    Value    Label       │            │
         │  │  ● blue      1      Day 1      │            │
         │  │  ● green     2      Day 2      │            │
         │  │  ● red       3      Day 3      │            │
         │  │  ● yellow    4      Day 4      │            │
         │  │  ● purple    5      Day 5      │            │
         │  │  ● orange    6      Day 6      │            │
         │  │  ● gray    (null)   Unassigned  │            │
         │  └─────────────────────────────────┘            │
         │                                                 │
         │                      [Apply]  [OK]              │
         └─────────────────────────────────────────────────┘

Step 4:  Look at the map. Ask yourself:
```

```
  GOOD clustering:                    BAD clustering:
  Day 2 POIs are grouped              Day 2 POIs are scattered

  ┌────────────────────┐              ┌────────────────────┐
  │                    │              │   ●2               │
  │     ●2 ●2         │              │         ●3         │
  │      ●2            │              │                    │
  │              ●3 ●3 │              │  ●2                │
  │              ●3    │              │        ●2    ●3    │
  │  ●1                │              │                    │
  │  ●1 ●1            │              │     ●2       ●1    │
  └────────────────────┘              └────────────────────┘
  → Efficient! Minimal walking.       → Lots of backtracking!
                                        Move some POIs to other days.
```

---

## 8. Measure Distance

```
Step 1:  Click the Measure tool in the toolbar (ruler icon 📏)
         Or: Menu → View → Measure → Measure Line

Step 2:  Click on POI A on the map

Step 3:  Click on POI B

Step 4:  Read the distance in the popup:

         ┌─ Measure ──────────────────┐
         │                            │
         │  Total: 1,247.3 m          │  ← straight-line distance
         │                            │
         │  Segments:                 │
         │    1: 1,247.3 m            │
         │                            │
         └────────────────────────────┘

Step 5:  Right-click to stop measuring

Note: This is straight-line ("as the crow flies") distance.
      Actual walking distance is typically 1.3-1.5x longer
      due to streets and turns.

      Rule of thumb:
      ┌────────────────────────────────────┐
      │  Straight-line    Walking estimate │
      │  500m          →  ~650-750m        │
      │  1,000m        →  ~1,300-1,500m    │
      │  2,000m        →  ~2,600-3,000m    │
      └────────────────────────────────────┘
```

---

## 9. Buffer Analysis (What's Near the Hotel?)

This creates a circle around a point showing what's within walking distance.

```
Step 1:  Menu → Vector → Geoprocessing Tools → Buffer...

         ┌─ Buffer ───────────────────────────────────────┐
         │                                                 │
         │  Input layer:   [ accommodation        ▼]      │
         │                                                 │
         │  Distance:      [ 500    ]                      │
         │  Units:         [ meters ▼]                     │
         │                                                 │
         │  Segments:      [ 36 ]  (smoothness of circle)  │
         │                                                 │
         │                  [Run]                           │
         └─────────────────────────────────────────────────┘

Step 2:  Click [Run]. A circle appears on the map!

Step 3:  Repeat with 1000m for a second ring.

         What you'll see on the map:

         ┌──────────────────────────────────────┐
         │                                      │
         │          . . . . . . .               │
         │        .    1km ring    .            │
         │       .   . . . . . .    .          │
         │      .  .  500m ring  .   .         │
         │     .  .              .    .        │
         │     .  .    🏨 hotel  .    .        │
         │     .  .    ●food     .    .        │
         │      .  . ●cultural .   .          │
         │       .   . . . . . .    .          │
         │        .  ●landmark    .            │
         │          . . . . . . .    ●shopping │
         │                           (too far!) │
         └──────────────────────────────────────┘

         Insight: POIs inside the 500m ring are easy
         walking. POIs outside 1km need metro/taxi.
```

---

## 10. Export a Print-Ready PDF Map

This creates your offline daily maps for the trip.

```
Step 1:  Set up the map view:
         - Zoom to show all Day 1 POIs
         - Turn off layers for other days
         - Make sure base map + relevant POIs are visible

Step 2:  Menu → Project → New Print Layout
         Give it a name: "Day 1 Map"

Step 3:  The Print Layout editor opens:

┌─ Print Layout: Day 1 Map ───────────────────────────────────────┐
│  Layout   Edit   View   Item   Atlas                             │
├─────────┬───────────────────────────────────────────────────────┤
│         │  ┌─────────────────────────────────────────────┐      │
│  TOOLS  │  │                                             │      │
│         │  │         (empty page — add items here)       │      │
│ [+Map]  │  │                                             │      │
│ [+Text] │  │                                             │      │
│ [+Leg.] │  │                                             │      │
│ [+Scale]│  │                                             │      │
│ [+Arrow]│  │                                             │      │
│         │  │                                             │      │
│         │  └─────────────────────────────────────────────┘      │
│         │                                                        │
├─────────┴───────────────────────────────────────────────────────┤
│  Page: A4 Landscape                                              │
└──────────────────────────────────────────────────────────────────┘

Step 4:  Add items to the page:

  a) Add Map:   Click [Add Map] tool → draw a rectangle on the page
                 The map canvas content appears inside it!

  b) Add Title: Click [Add Label] → draw a box at the top
                 Type: "Day 1 — Arrival & The Bund"

  c) Add Legend: Click [Add Legend] → draw a box in the corner
                 Auto-populates from visible layers

  d) Add Scale:  Click [Add Scale Bar] → draw at the bottom
                 Shows distance reference

Step 5:  Your layout should look like:

         ┌──────────────────────────────────────────────┐
         │                                              │
         │   Day 1 — Arrival & The Bund                 │
         │                                              │
         │   ┌──────────────────────────────────┐       │
         │   │           MAP                    │       │
         │   │                                  │       │
         │   │    ●  The Bund                   │       │
         │   │    ●  Oriental Pearl Tower       │       │
         │   │    ●  Nanjing Road               │       │
         │   │                                  │       │
         │   │    ---- walking route ----       │       │
         │   │                                  │       │
         │   └──────────────────────────────────┘       │
         │                                              │
         │   LEGEND          ├──── 500m ────┤           │
         │   ● Landmark                                 │
         │   ● Food                                     │
         │   ● Shopping          Shanghai Trip 2026     │
         │                                              │
         └──────────────────────────────────────────────┘

Step 6:  Export!
         Menu → Layout → Export as PDF
         Save to: offline/day-1.pdf

Step 7:  Repeat for Days 2-6.
```

---

## 11. Save Your QGIS Project

Always save your QGIS project so you don't have to reload layers next time.

```
Menu → Project → Save As...
Save to: shanghai-trip-gis/qgis/shanghai-trip.qgz

What's saved:
  ✓ Which layers are loaded
  ✓ Layer styles and colors
  ✓ Map zoom and position
  ✓ Print layouts

What's NOT saved (it's in the GeoJSON files):
  ✗ The actual POI data
```

---

## Quick Reference Card

Print this or keep it open while working in QGIS.

```
┌─────────────────────────────────────────────────────────┐
│                QGIS QUICK REFERENCE                      │
├──────────────────────┬──────────────────────────────────┤
│  ADD DATA            │  Layer → Add Vector Layer        │
│                      │  Or drag .geojson into Layers    │
├──────────────────────┼──────────────────────────────────┤
│  ADD BASE MAP        │  Browser → XYZ Tiles → OSM      │
├──────────────────────┼──────────────────────────────────┤
│  ZOOM TO LAYER       │  Right-click layer → Zoom to    │
├──────────────────────┼──────────────────────────────────┤
│  IDENTIFY (click)    │  Toolbar → ℹ️ icon → click POI  │
├──────────────────────┼──────────────────────────────────┤
│  MEASURE DISTANCE    │  Toolbar → 📏 icon              │
│                      │  Click A, click B, right-click   │
├──────────────────────┼──────────────────────────────────┤
│  CHANGE COLORS       │  Right-click layer → Properties  │
│                      │  → Symbology → set color         │
├──────────────────────┼──────────────────────────────────┤
│  COLOR BY CATEGORY   │  Properties → Symbology          │
│                      │  → Categorized → Column: day     │
│                      │  → Classify                      │
├──────────────────────┼──────────────────────────────────┤
│  BUFFER              │  Vector → Geoprocessing → Buffer │
│                      │  Distance: 500, Units: meters    │
├──────────────────────┼──────────────────────────────────┤
│  PRINT / PDF         │  Project → New Print Layout      │
│                      │  Add map, title, legend, scale   │
│                      │  Layout → Export as PDF           │
├──────────────────────┼──────────────────────────────────┤
│  SAVE PROJECT        │  Project → Save As → .qgz        │
├──────────────────────┼──────────────────────────────────┤
│  UNDO                │  Ctrl+Z  (Cmd+Z on Mac)          │
│  ZOOM ALL            │  Ctrl+Shift+F                    │
│  PAN                 │  Hold spacebar + drag            │
└──────────────────────┴──────────────────────────────────┘
```

---

## Common Gotchas

```
PROBLEM                          FIX
──────────────────────────────   ────────────────────────────────
Map is blank after adding        Right-click layer → Zoom to Layer
a layer                          (your data might be off-screen)

POIs appear in the ocean         You swapped lat/lng in GeoJSON
                                 Should be [lng, lat] = [121.x, 31.x]

"CRS mismatch" warning          Click OK. Our files are WGS84
                                 (EPSG:4326) which matches OSM.

Buffer creates a tiny circle     Check units — use meters, not degrees.
                                 Distance: 500, Units: meters

Can't click to identify          Make sure the ℹ️ Identify tool is
                                 selected, not the Pan 🖐 tool

Print layout is blank            After adding a map item, click
                                 "Set Map Extent to Match Main
                                 Canvas Extent" in item properties

Layer changes don't appear       Did you click [Apply] in the
on the map                       Properties dialog? Easy to forget.
```
