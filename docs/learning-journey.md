# GIS Learning Journey

```
  ┌─────────────────────────────────────────────────────────┐
  │                  LEARNING PATH                           │
  │                                                         │
  │  Module 1 ──→ Module 2 ──→ Module 3 ──→ Module 4       │
  │  What is       Coordinates   GeoJSON &    Analysis &    │
  │  GIS?          & Projections Spatial Data  Print Maps   │
  │                                                         │
  │  ──→ Module 5a ──→ Module 5b ──→ Module 6 ──→ Module 7 │
  │      Read the      Build &       Cartographic  Story    │
  │      web map       deploy        design        map      │
  │                                                         │
  │  ⏱ ~18-22 hours total across all modules                │
  │  👥 Pair learning: both people work together             │
  └─────────────────────────────────────────────────────────┘
```

A structured 7-module curriculum for 2 people. Each module combines theory, hands-on practice, and a project deliverable. Work through modules together as pair learning sessions — discuss, explore, and help each other.

---

## Module 1 -- What is GIS? (Phase 0, Week 1)

**Estimated time: 1-1.5 hours | Both people**

### Concepts
- What Geographic Information Systems are and why they matter
- Real-world GIS applications in tourism and sustainability
- The 3 building blocks: **data**, **analysis**, **visualization**
- Raster vs. Vector data (we'll focus on vector)

### Hands-On (~45 min)
1. Open [OpenStreetMap](https://www.openstreetmap.org/) and explore Shanghai together (~10 min)
2. Open [Overpass Turbo](https://overpass-turbo.eu/) and run a simple query (~15 min):
   ```
   node["tourism"="attraction"](31.1,121.3,31.4,121.6);
   out body;
   ```
   You just ran your first spatial query — it finds all tourist attractions in Shanghai!
3. Explore [kepler.gl demo](https://kepler.gl/demo) to see what's possible with GIS visualization (~20 min)

### Deliverable
- Discuss together: "What surprised us about GIS? How could this apply to sustainable tourism?"

### Self-Check
- [ ] I can explain what GIS stands for and why it's useful
- [ ] I understand the difference between raster and vector data
- [ ] I successfully ran a spatial query on Overpass Turbo

---

## Module 2 -- Coordinates & Projections (Phase 0, Week 1-2)

**Estimated time: 1.5 hours | Both people**

### Concepts
- Latitude and longitude -- how every point on Earth gets an address
- WGS84 (EPSG:4326) -- the coordinate system GPS and GeoJSON use
- Why maps distort the Earth, and why we mostly don't worry at city scale
- **The GeoJSON gotcha:** `[lng, lat]` not `[lat, lng]`!
- **China's GCJ-02 offset** -- why we avoid Chinese tile providers (see [architecture.md](architecture.md#8-gcj-02-coordinate-offset-strategy))

```
  ⚠  THE #1 BEGINNER MISTAKE:

  Google Maps shows:    31.2304, 121.4737   (lat, lng)
  GeoJSON needs:       [121.4737, 31.2304]  (lng, lat)
                        ↑ swap!              ↑ swap!
```

### Hands-On (~45 min)
1. Find coordinates of a favorite Shanghai spot on Google Maps (~10 min)
2. Swap the order and plot 3 points on [geojson.io](https://geojson.io/) (~15 min)
3. Open QGIS, add OpenStreetMap base layer, zoom to Shanghai (~15 min)
4. Verify your points appear in the right locations on both tools (~5 min)

### Deliverable
- Each person creates 1 POI on geojson.io and pushes it to the repo

### Self-Check
- [ ] I can find coordinates for any location using Google Maps
- [ ] I know why GeoJSON uses `[lng, lat]` instead of `[lat, lng]`
- [ ] I can explain why we don't use Chinese map tiles (GCJ-02)
- [ ] I successfully opened QGIS and loaded a base map

---

## Module 3 -- GeoJSON & Spatial Data (Phase 1, Week 3)

**Estimated time: 2-2.5 hours | Both people**

### Concepts

```
  THREE GEOMETRY TYPES:

  Point               LineString           Polygon
  (a location)        (a path)             (an area)

       ●              ●───●───●            ●───●
                          │               │     │
  POI marker          Walking route       ●───●
                                          District
```

- GeoJSON specification: Features, FeatureCollections, geometry types
- Properties -- attaching information to geometry (name, category, etc.)
- Our POI schema: `id`, `name_en`, `name_cn`, `category`, `day`, `priority`
- See [contribution-guide.md](contribution-guide.md#allowed-values-reference) for allowed values

### Hands-On (~1.5 hours)
1. Open a `.geojson` file in VS Code -- read the structure (~15 min)
2. Add full properties to a point: `id`, `name_en`, `name_cn`, etc. (~15 min)
3. Create a walking route as a LineString on geojson.io (~15 min)
4. Draw a polygon around a neighborhood on geojson.io (~15 min)
5. Load all three types into QGIS -- see them as separate layers (~15 min)
6. Validate at [geojsonlint.com](https://geojsonlint.com/) (~5 min)

### Deliverable
- Each person adds 5-8 POIs to their primary category files with full properties
- Person 1 creates a test route (LineString) between 2 POIs
- Person 2 creates a test area (Polygon) around a district

### Self-Check
- [ ] I can explain the difference between a Feature and a FeatureCollection
- [ ] I know Point, LineString, and Polygon geometry types
- [ ] I can write a valid POI with all required properties
- [ ] My GeoJSON passes validation

---

## Module 4 -- Spatial Analysis & Print Maps (Phase 2, Week 4-5)

**Estimated time: 3-4 hours (spread across 2 weeks) | Both people, Person 2 leads sustainability**

### Concepts
- **Distance calculation** -- how far is A from B?
- **Buffers** -- "show me everything within 500m of the hotel"
- **Clustering** -- are our POIs grouped efficiently or scattered?
- **Print layouts** -- exporting maps as PDFs for offline use
- **Sustainability analysis** -- transport mode mix and CO2 estimates

### Hands-On: Analysis (in QGIS, ~1.5 hours)

Both people work through these together:

1. **Measure distance:** Use the measure tool between Day 1 POIs (~20 min)
2. **Buffer:** Create 500m and 1km buffers around the hotel (~30 min)
   - `Vector -> Geoprocessing -> Buffer`
3. **Cluster check:** Color POIs by day -- are same-day POIs grouped? (~20 min)

```
  GOOD clustering:                 BAD clustering:
  ┌──────────────────┐             ┌──────────────────┐
  │      ●2 ●2       │             │   ●2          ●3 │
  │       ●2         │             │        ●2        │
  │           ●3 ●3  │             │  ●3       ●2     │
  │           ●3     │             │     ●3           │
  │ ●1               │             │  ●1       ●2     │
  │ ●1 ●1            │             │        ●1        │
  └──────────────────┘             └──────────────────┘
  Each day is compact.             Days are scattered!
  Minimal walking.                 Reassign some POIs.
```

### Hands-On: Print Layout (~1.5 hours)

Person 1 creates the template; Person 2 uses it to export remaining days:

4. **Create Day 1 PDF:** `Project -> New Print Layout` (~45 min for first one)
5. **Export remaining days** using the same template (~20 min each)

### Sustainability Analysis (Person 2 leads, ~1.5 hours)

6. **Run the CO2 calculator:** `python3 tools/co2-calculator.py` — generates per-day and trip-total emissions using Shanghai-specific emission factors. Review the output in `data/analysis/co2-summary.json` (~15 min)
7. **Apply the sustainability scorecard** to 20+ relevant POIs using the criteria in [sustainability-methodology.md](sustainability-methodology.md): transit_access, heritage_value, community_impact, walkability, environmental_sensitivity (~30 min)
8. **Transit accessibility analysis:** Follow [transit-analysis-guide.md](transit-analysis-guide.md) to create 800m metro station buffers and calculate what % of POIs are transit-accessible (SDG 11.2) (~30 min)
9. **Add `sustainability_notes`** to POIs where relevant — use sourced observations, not marketing copy (~15 min)

```
  CO2 REFERENCE (per person per km):
  ┌──────────────┬──────────────────┐
  │  Walking     │     0 g          │
  │  Metro       │   ~40 g          │
  │  Bus         │   ~80 g          │
  │  Taxi        │  ~150 g          │
  └──────────────┴──────────────────┘

  Example Day 2:
  Hotel → Yu Garden (metro, 3km)     = 120g
  Yu Garden → Nanxiang (walk, 0.2km) =   0g
  Nanxiang → Tianzifang (metro, 4km) = 160g
  Tianzifang → Hotel (taxi, 5km)     = 750g
  ─────────────────────────────────────
  Day 2 total:                       1,030g = ~1kg CO2
```

### Deliverable
- Buffer layer around hotel exported as GeoJSON
- Daily distance estimates documented
- At least one itinerary improvement based on analysis
- PDF maps for all 6 days
- Transport mode audit and CO2 summary (Person 2)

### Self-Check
- [ ] I can measure distances between points in QGIS
- [ ] I created a buffer and understand what it shows
- [ ] I can visually assess whether a day's POIs are clustered
- [ ] I exported at least one print-ready PDF map
- [ ] (Person 2) I ran the CO2 calculator and reviewed the output
- [ ] (Person 2) I scored at least 10 POIs using the sustainability scorecard
- [ ] (Person 2) I completed the transit accessibility analysis (800m buffers)

### Advanced Extras (Optional)
- **Spatial join:** Auto-fill "district" for each POI
- **Nearest neighbor:** Find each POI's closest neighbor

---

## Module 5a -- Understanding the Web Map (Phase 3, Week 5-6)

**Estimated time: 2 hours | Both people, Person 1 leads**

```
  This module uses a STARTER TEMPLATE that already works.
  Your job: understand it and customize it — not build from scratch.

  Person 1 (Lead) walks Person 2 through the code.
  Person 2 makes at least one modification by the end.
```

### Concepts
- How web maps work: tiles, layers, zoom levels
- What HTML, CSS, and JavaScript do
- Leaflet.js basics: map object, tile layers, markers, popups
- Loading GeoJSON data into a web map

### Hands-On (~1.5 hours)
1. Open `web/index.html` in Chrome via Live Server -- see the working map (~5 min)
2. Read through the code in VS Code -- focus on structure, not every line (~20 min)
3. Change the starting view coordinates to center on your hotel (~10 min)
4. Swap the base map style (try different CartoDB options) (~10 min)
5. Load a different POI file -- see your data appear (~20 min)
6. Customize a popup -- change what info appears when you click (~20 min)
7. **Person 2:** Make one modification on your own (e.g., change a color, edit popup text) (~15 min)

### Deliverable
- The starter template loads your real POI data from at least 2 category files
- Popups show Chinese name, category, and description
- Person 2 has made at least one independent code modification

### Self-Check
- [ ] I can explain what tiles are and why maps load in squares
- [ ] I can change the map's center point and zoom level
- [ ] I successfully loaded real GeoJSON data onto the web map
- [ ] (Person 2) I made at least one code change on my own

---

## Module 5b -- Building Features & Deploying (Phase 3, Week 6-7)

**Estimated time: 3-4 hours | Person 1 leads, Person 2 reviews**

### Concepts
- Layer groups and layer controls in Leaflet.js
- Styling GeoJSON features (custom icons, colored lines)
- Making web pages responsive for mobile
- Deploying to GitHub Pages

### Hands-On (Person 1 builds, Person 2 tests, ~3 hours)
1. Load all POI categories as separate layer groups (~30 min)
2. Add layer toggle controls (`L.control.layers`) (~30 min)
3. Add day filter buttons (~30 min)
4. Add route lines for each day (~20 min)
5. Custom colored markers for each category (~30 min)
6. **Person 2 tests on mobile:** check popup sizes, touch targets, Chinese names (~20 min)
7. Deploy to GitHub Pages (~20 min)

### Deliverable
- Working web map with all categories, layer toggles, and day filter
- Deployed and accessible on phones
- Person 2 has tested and reported 3+ findings

### Self-Check
- [ ] Layer toggle controls work (show/hide categories)
- [ ] Day filter correctly fades non-selected POIs
- [ ] The map works on a phone screen
- [ ] The map is deployed at a public URL

---

## Module 6 -- Cartographic Design (Phase 4, Week 7-8)

**Estimated time: 2-3 hours | Both people**

### Concepts
- Map design principles: hierarchy, contrast, simplicity
- Color theory for maps (colorblind-friendly palettes)
- Legend design
- The difference between a "map" and a "good map"

### Hands-On (~2 hours)

Both people do a **pair review** of the web map:

1. Review critically: What's cluttered? Hard to read? (~15 min)
2. Apply a consistent color palette ([ColorBrewer](https://colorbrewer2.org/)) (~20 min)
3. Design a clean legend (~20 min)
4. Improve popups -- is the Chinese name prominent enough? (~20 min)
5. Export a "hero image" from QGIS for portfolio (~30 min)

```
  THE DESIGN TEST:
  ┌──────────────────────────────────────────┐
  │  Show the map to someone who hasn't      │
  │  seen it before. Ask:                    │
  │                                          │
  │  "What is this map showing?"             │
  │                                          │
  │  If they can answer correctly in          │
  │  5 seconds → good design                 │
  │  If they're confused → needs work         │
  └──────────────────────────────────────────┘
```

### Deliverable
- Polished web map with intentional design choices
- One QGIS print layout exported as PNG/PDF (portfolio hero image)
- Each person can explain one design decision they contributed

### Self-Check
- [ ] I can name 3 principles of good map design
- [ ] I chose a colorblind-friendly palette and can explain why
- [ ] The Chinese name is the most prominent text in each popup
- [ ] I exported a portfolio-quality map image from QGIS

---

## Module 7 -- Story Map (Phase 6, Post-Trip)

**Estimated time: 2-3 hours | Both people, Person 2 leads narrative**

```
  STORY MAP = maps + photos + narrative

  ┌─────────────────────────────────┐
  │  Hero: "Shanghai & Suzhou"      │
  │  ┌───────────────────────────┐  │
  │  │  Day 1 Map   │ Narrative  │  │
  │  │  ● ● ●       │ "We       │  │
  │  │              │ arrived..."│  │
  │  ├───────────────┤           │  │
  │  │  📷 📷 📷     │           │  │
  │  └───────────────┴───────────┘  │
  │  Day 2...                       │
  │  Day 3...                       │
  │  ┌───────────────────────────┐  │
  │  │  Sustainability Reflection│  │ ← Person 2
  │  │  GIS Methodology Reflect. │  │ ← Person 1
  │  └───────────────────────────┘  │
  └─────────────────────────────────┘
```

### Concepts
- Story maps as a GIS communication tool
- Narrative cartography -- maps that tell stories
- Portfolio presentation -- framing work for an audience

### Hands-On (~2 hours)

| Task | Owner |
|------|-------|
| Gather photos, GPS traces, trip notes | Both |
| Open `web/story-template.html`, read placeholders | Both |
| Fill in day-by-day narrative | Person 2 |
| Add GPS traces as actual-route layers | Person 1 |
| Write sustainability reflection (SDG 11/12) | Person 2 |
| Write GIS methodology reflection | Person 1 |
| Final polish and screenshots | Both |

### Deliverable
- Completed story map with photos, notes, and real trip data
- Sustainability reflection connecting GIS findings to SDGs
- Portfolio-ready screenshots

### Self-Check
- [ ] Each day has at least one photo and a short narrative
- [ ] The story map loads and scrolls correctly
- [ ] (Person 2) Sustainability reflection connects to SDG 11 or 12
- [ ] (Person 1) GIS methodology reflection explains tools and techniques used
- [ ] I have at least one portfolio-quality screenshot

---

## Skills Matrix

```
  By the end, both people will have practiced:

  Skill                          Module  Tool
  ────────────────────────────────────────────────
  Understanding GIS concepts     1       Discussion
  Reading coordinates            2       Google Maps, geojson.io
  Creating spatial data          3       geojson.io, VS Code
  Using desktop GIS software     4       QGIS
  Spatial analysis               4       QGIS
  Creating print maps            4       QGIS Print Layout
  Sustainability analysis        4       QGIS + spreadsheet
  Reading web map code           5a      Leaflet.js, HTML/CSS/JS
  Building web map features      5b      Leaflet.js, GitHub Pages
  Cartographic design            6       QGIS, Leaflet.js
  Version control                All     Git, GitHub Desktop
  Real-world data collection     Trip    Phone GPS, camera
  Storytelling with maps         7       Story map template
```
