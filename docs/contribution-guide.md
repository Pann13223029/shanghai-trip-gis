# Contribution Guide

A step-by-step guide for adding data and making changes to the Shanghai Trip GIS project. Written for beginners — no prior Git or GIS experience needed.

---

## Getting Started (One-Time Setup)

### 1. Install Tools

| Tool | Download | Purpose |
|------|----------|---------|
| GitHub Desktop | [desktop.github.com](https://desktop.github.com/) | Push/pull changes without command line |
| QGIS | [qgis.org/download](https://qgis.org/en/site/forusers/download.html) | Desktop GIS for analysis |
| VS Code | [code.visualstudio.com](https://code.visualstudio.com/) | Text editor for GeoJSON files |
| Chrome | Already have it | Testing the web map |

### 2. Clone the Repository

1. Open **GitHub Desktop**
2. Click **File -> Clone Repository**
3. Select `shanghai-trip-gis` from the list (or paste the repo URL)
4. Choose a local folder and click **Clone**

### 3. Open in VS Code

1. In GitHub Desktop, click **Open in Visual Studio Code**
2. Install the recommended extension: **GeoJSON Map Preview** (lets you see your GeoJSON on a map inside VS Code)

---

## File Ownership

**Each member owns specific files.** Only edit files assigned to you. This prevents merge conflicts (the #1 source of beginner Git frustration).

| Member | Owned Files | Categories |
|--------|-------------|------------|
| Member A | `landmarks.geojson`, `accommodation.geojson` | Landmarks, Accommodation |
| Member B | `food.geojson`, `transport.geojson` | Food, Transport |
| Member C | `shopping.geojson`, `cultural.geojson` | Shopping, Cultural/Historical |
| Member D | `nature.geojson`, `suzhou.geojson` | Nature/Parks, Suzhou |

**What if I find a great restaurant but I own landmarks?**
Tell Member B (the food file owner) and they'll add it. You can share the details in the group chat — name, coordinates, description — and the owner enters it. This mirrors how professional GIS teams work.

---

## Allowed Values Reference

Use ONLY these values for constrained fields. Using other values will cause filtering bugs on the map.

| Field | Allowed Values |
|-------|---------------|
| `category` | `landmark`, `food`, `shopping`, `cultural`, `nature`, `transport`, `accommodation` |
| `priority` | `must-visit`, `nice-to-have`, `optional` |
| `day` | `1`, `2`, `3`, `4`, `5`, `6`, or `null` (undecided) |
| `weather_sensitive` | `true` (outdoor/exposed), `false` (indoor/covered) |
| `mode` (routes) | `walking`, `metro`, `taxi`, `bus`, `train` |

---

## Adding a New Point of Interest (POI)

### Method A: Using geojson.io (Easiest)

1. Go to [geojson.io](https://geojson.io/)
2. Navigate to Shanghai
3. Click the **marker tool** and place your point on the map
4. In the right panel, edit the properties:
   ```json
   {
     "id": "cultural-001",
     "name_en": "Yu Garden",
     "name_cn": "豫园",
     "category": "cultural",
     "day": 2,
     "description": "Classical Chinese garden from the Ming Dynasty",
     "address": "218 Anren St, Huangpu District",
     "est_duration_min": 90,
     "est_cost_cny": 40,
     "opening_hours": "8:30-17:00",
     "priority": "must-visit",
     "weather_sensitive": false,
     "added_by": "your_name",
     "last_verified": "2026-03",
     "sustainability_notes": "",
     "photos": [],
     "notes": ""
   }
   ```
5. Click **Save -> GeoJSON** and download the file
6. Open the downloaded file, **copy just the Feature** (not the whole FeatureCollection)
7. Paste it into YOUR assigned category file in `data/poi/` (e.g., `cultural.geojson`)

### Method B: Editing GeoJSON Directly

1. Open YOUR assigned file in `data/poi/` (e.g., `food.geojson`)
2. Find the `"features": [...]` array
3. Add a new Feature object:
   ```json
   {
     "type": "Feature",
     "geometry": {
       "type": "Point",
       "coordinates": [121.4925, 31.2272]
     },
     "properties": {
       "id": "food-001",
       "name_en": "Nanxiang Steamed Bun Restaurant",
       "name_cn": "南翔馒头店",
       "category": "food",
       "day": 2,
       "description": "Famous xiaolongbao since 1900, next to Yu Garden",
       "address": "85 Yuyuan Rd, Huangpu District",
       "est_duration_min": 45,
       "est_cost_cny": 30,
       "opening_hours": "9:00-21:00",
       "priority": "must-visit",
       "weather_sensitive": false,
       "added_by": "your_name",
       "last_verified": "2026-03",
       "sustainability_notes": "",
       "photos": [],
       "notes": ""
     }
   }
   ```
4. Remember: coordinates are `[longitude, latitude]` — lng first!

### How to Find Coordinates

**Before the trip (use Google Maps):**
1. Open [Google Maps](https://maps.google.com)
2. Search for the place
3. Right-click on the exact location -> the coordinates appear (e.g., `31.2272, 121.4925`)
4. **Swap the order** for GeoJSON: `[121.4925, 31.2272]` (lng, lat)

**During the trip in China (use Dianping or Amap):**
Google Maps is blocked in China. Use Dianping (大众点评) for restaurants or Amap (高德地图) for general places. See [architecture.md — China Tech Constraints](architecture.md#china-tech-constraints).

### ID Assignment

Each POI needs a unique ID in the format `{category}-{nnn}`:
- Check your file for the highest existing number
- Use the next number: if the last entry is `food-007`, your new entry is `food-008`
- IDs are zero-padded to 3 digits: `001`, `002`, ..., `099`, `100`

---

## Pushing Your Changes

### Step-by-Step (GitHub Desktop)

1. **Before you start editing**, click **Fetch origin** in GitHub Desktop to get the latest changes
2. Edit ONLY your assigned files
3. When done, open **GitHub Desktop**
4. You'll see your changed files in the left panel
5. **Verify** you only changed files you own (if you see someone else's file, undo it)
6. Write a short description in the **Summary** box:
   - Good: `Add 5 food POIs in Huangpu district`
   - Bad: `update`
7. Click **Commit to main**
8. Click **Push origin**

### Before You Push — Checklist

- [ ] I only edited files assigned to me
- [ ] Every POI has a unique `id` in the correct format
- [ ] Coordinates are in `[longitude, latitude]` order
- [ ] Coordinates place the marker at the correct building (verified on geojson.io satellite view)
- [ ] `name_cn` is filled in (use Google Translate or Dianping if needed)
- [ ] `category` matches the filename (food POI in `food.geojson`)
- [ ] `priority` is one of: `must-visit`, `nice-to-have`, `optional`
- [ ] `day` is 1-6 or `null`
- [ ] `added_by` has your name
- [ ] The file is still valid JSON (validated at geojsonlint.com)

### Validating Your GeoJSON

Paste your file contents into [geojsonlint.com](https://geojsonlint.com/) to check for errors. A GitHub Action will also validate your files automatically after you push — if you see a red X on your commit, check the action log.

### If Something Goes Wrong

- **"Conflict" message in GitHub Desktop** -> Don't try to resolve it yourself. Tell the team lead. This usually means someone edited a file that isn't theirs.
- **Red X on your commit in GitHub** -> Your GeoJSON has a syntax error. Open the file, paste it into geojsonlint.com, fix the error, commit again.
- **Accidentally edited the wrong file** -> In GitHub Desktop, right-click the file and choose "Discard changes."

---

## Rotating Roles

Each project phase, you'll take on a different role:

### Data Collector
- Research places to visit using travel blogs, Dianping, Google Maps, and recommendations
- Add POIs to YOUR assigned GeoJSON files with complete properties
- Verify coordinates are accurate (check satellite view on geojson.io)

### Cartographer
- Style map layers in QGIS (colors, icons, labels)
- Design the visual look of the web map
- Create print layouts for offline backup PDFs
- Ensure the map is readable and beautiful

### Web Dev
- Build and maintain the Leaflet.js web application (starting from the provided template)
- Add new features (layer toggles, popups, day filter)
- Test on mobile devices
- Deploy updates to GitHub Pages

### Analyst
- Run spatial analysis in QGIS (distances, buffers, cluster visualization)
- Optimize daily itineraries based on geographic efficiency
- Generate analysis outputs (distance tables, buffer maps)
- Present findings to the group for itinerary decisions

---

## File Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| POI data | `data/poi/{category}.geojson` | `data/poi/food.geojson` |
| Route data | `data/routes/day-{n}.geojson` | `data/routes/day-1.geojson` |
| Area data | `data/areas/{name}.geojson` | `data/areas/districts.geojson` |
| Offline PDFs | `offline/day-{n}.pdf` | `offline/day-1.pdf` |
| Photos | `web/assets/photos/{day}/{name}.jpg` | `web/assets/photos/day-1/bund-sunset.jpg` |

---

## Getting Help

- **GeoJSON syntax error?** -> Paste into [geojsonlint.com](https://geojsonlint.com/)
- **Can't find coordinates?** -> Right-click on Google Maps (pre-trip) or use Amap (in China)
- **Git conflict?** -> Tell the team lead. Do NOT try to resolve it yourself.
- **Accidentally edited wrong file?** -> Right-click -> Discard changes in GitHub Desktop
- **QGIS is confusing?** -> Check the [QGIS Training Manual](https://docs.qgis.org/3.34/en/docs/training_manual/)
- **Leaflet question?** -> Check the [Leaflet Tutorials](https://leafletjs.com/examples.html)
- **Need Chinese name for a place?** -> Search on [Dianping](https://www.dianping.com/) or [Baidu Maps](https://map.baidu.com/)
