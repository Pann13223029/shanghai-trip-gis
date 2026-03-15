# GIS Learning Journey

A structured 7-module curriculum woven into the project phases. Each module combines theory, hands-on practice, and a project deliverable so learning directly contributes to the trip map.

---

## Module 1 -- What is GIS? (Phase 0, Week 1)

**Estimated time: 1.5-2 hours**

### Concepts
- What Geographic Information Systems are and why they matter
- Real-world GIS applications in tourism and sustainability
- The 3 building blocks: **data**, **analysis**, **visualization**
- Raster vs. Vector data (we'll focus on vector)

### Hands-On (~45 min)
1. Open [OpenStreetMap](https://www.openstreetmap.org/) and explore Shanghai (~10 min)
2. Open [Overpass Turbo](https://overpass-turbo.eu/) and run a simple query (~15 min):
   ```
   node["tourism"="attraction"](31.1,121.3,31.4,121.6);
   out body;
   ```
   This finds all tourist attractions in Shanghai -- you just ran your first spatial query!
3. Explore [kepler.gl demo](https://kepler.gl/demo) to see what's possible with GIS visualization (~20 min)

### Deliverable
- Each member writes 2-3 sentences: "What surprised me about GIS?" (add to a shared discussion)

### Self-Check
- [ ] I can explain what GIS stands for and why it's useful
- [ ] I understand the difference between raster and vector data
- [ ] I successfully ran a spatial query on Overpass Turbo

---

## Module 2 -- Coordinates & Projections (Phase 0, Week 1-2)

**Estimated time: 1.5-2 hours**

### Concepts
- Latitude and longitude -- how every point on Earth gets an address
- WGS84 (EPSG:4326) -- the coordinate system GPS and GeoJSON use
- Why maps distort the Earth (projections), and why we mostly don't worry about it at city scale
- How to read coordinates: `[121.4737, 31.2304]` = [longitude, latitude] (GeoJSON order!)
- **China's GCJ-02 offset** -- Chinese maps deliberately shift coordinates by 200-400m. Our project uses WGS84 only (see [architecture.md](architecture.md#8-gcj-02-coordinate-offset-strategy))

### Hands-On (~45 min)
1. Find the coordinates of a favorite Shanghai spot on Google Maps (right-click -> coordinates) (~10 min)
2. Notice: Google shows `lat, lng` but GeoJSON uses `[lng, lat]` -- a classic gotcha! (~5 min)
3. Plot 3 points on [geojson.io](https://geojson.io/) and inspect the generated GeoJSON (~15 min)
4. Open QGIS, add OpenStreetMap as a base layer, and zoom to Shanghai (~15 min)

### Deliverable
- Each member creates 1 POI on geojson.io and saves it as a `.geojson` file
- Push it to the repo in `data/poi/`

### Self-Check
- [ ] I can find coordinates for any location using Google Maps
- [ ] I know why GeoJSON uses `[lng, lat]` instead of `[lat, lng]`
- [ ] I can explain why we don't use Chinese map tiles in our web map (GCJ-02)
- [ ] I successfully opened QGIS and loaded a base map

---

## Module 3 -- GeoJSON & Spatial Data (Phase 1, Week 3)

**Estimated time: 2-3 hours**

### Concepts
- GeoJSON specification: Features, FeatureCollections, geometry types
- **Point** -- a single location (POI)
- **LineString** -- a path/route
- **Polygon** -- an area/boundary
- Properties -- attaching information to geometry (name, category, description)
- Feature Collections -- grouping multiple features into one file
- Our POI schema: `id`, `name_en`, `name_cn`, `category`, `day`, `priority` (see [contribution-guide.md](contribution-guide.md#allowed-values-reference))

### Hands-On (~1.5 hours)
1. Open a `.geojson` file in a text editor -- read the structure (~15 min)
2. Add properties to a point: `id`, `name_en`, `name_cn`, `category`, `description` (~15 min)
3. Create a simple walking route as a LineString on geojson.io (click multiple points) (~15 min)
4. Draw a polygon around a neighborhood on geojson.io (~15 min)
5. Load all three geometry types into QGIS -- see them as separate layers (~15 min)
6. Validate your GeoJSON at [geojsonlint.com](https://geojsonlint.com/) (~5 min)

### Deliverable
- Each member adds 5-10 POIs to their assigned category file with full properties
- One member creates a test route (LineString) between 2 POIs
- One member creates a test area (Polygon) around a district

### Self-Check
- [ ] I can explain the difference between a Feature and a FeatureCollection
- [ ] I know Point, LineString, and Polygon geometry types
- [ ] I can write a valid POI with all required properties
- [ ] My GeoJSON passes validation at geojsonlint.com

---

## Module 4 -- Spatial Analysis & Print Maps (Phase 2, Week 4-5)

**Estimated time: 3-4 hours (spread across 2 weeks)**

### Concepts
- **Distance calculation** -- how far is A from B? (straight-line vs. walking)
- **Buffers** -- "show me everything within 500m of the hotel"
- **Clustering** -- are our POIs grouped efficiently or scattered?
- **Print layouts** -- exporting maps from QGIS as PDFs for offline use
- Why analysis matters: turning raw data into actionable decisions

### Hands-On: Analysis (in QGIS, ~1.5 hours)
1. **Measure distance:** Use the measure tool to check walking distances between Day 1 POIs (~20 min)
   - `View -> Panels -> check "Sketching"` or use the ruler tool in toolbar
2. **Buffer:** Create a 500m and 1km buffer around the hotel POI (~30 min)
   - `Vector -> Geoprocessing -> Buffer`
   - This answers: "What's within easy walking distance of where we sleep?"
3. **Cluster check:** Visualize POIs colored by day -- are same-day POIs near each other? (~20 min)
   - Style the layer: `Right-click -> Properties -> Symbology -> Categorized -> Column: day`
   - If Day 3 POIs are scattered across the city, consider reassigning some

### Hands-On: Print Layout (in QGIS, ~1.5 hours)
4. **Create a daily PDF map:** Export Day 1's itinerary as a print-ready PDF (~45 min)
   - `Project -> New Print Layout`
   - Add map, title, legend, and scale bar
   - Export as PDF: `Layout -> Export as PDF`
5. **Repeat** for remaining days (these become your offline backup maps) (~30 min each after the first)

### Optional: Sustainability Enrichment
For the team member interested in sustainability analysis:
- Calculate what percentage of each day's transport is walking/metro vs. taxi
- Compare daily CO2 estimates by transport mode (walking = 0, metro ~ 40g/km, taxi ~ 150g/km per person)
- Add `sustainability_notes` to POIs where relevant (e.g., "locally sourced ingredients", "accessible via Line 2")

### Deliverable
- Buffer layer around hotel exported as GeoJSON
- Daily distance estimates documented
- At least one itinerary improvement based on analysis
- PDF maps for all 6 days (offline fallback for the trip)

### Self-Check
- [ ] I can measure distances between points in QGIS
- [ ] I created a buffer and understand what it shows
- [ ] I can visually assess whether a day's POIs are clustered or scattered
- [ ] I exported at least one print-ready PDF map from QGIS

### Advanced Extras (Optional)
These are powerful QGIS features you can explore if you finish early or want to go deeper:
- **Spatial join:** Join district polygons to POIs to auto-fill "district" property (`Vector -> Data Management -> Join attributes by location`)
- **Nearest neighbor:** For each POI, find the next closest POI (`Processing -> Distance to nearest hub`)

---

## Module 5a -- Understanding Web Maps (Phase 3, Week 5-6)

**Estimated time: 2-3 hours**

This module uses a **starter template** that already works. Your job is to understand it and customize it -- not to build from scratch.

### Concepts
- How web maps work: tiles, layers, zoom levels
- What HTML, CSS, and JavaScript do (the 3 languages of the web)
- Leaflet.js basics: map object, tile layers, markers, popups
- Loading external data (GeoJSON files) into a web map

### Hands-On (~2 hours)
1. **Open the starter template:** Open `web/index.html` in Chrome. You should see a working map of Shanghai with sample markers (~5 min)
2. **Read the code:** Open `web/index.html` in VS Code. Read through the comments. Don't worry about understanding every line -- focus on the structure (~20 min)
3. **Change the starting view:** Find the `setView` line and change the coordinates to center on your hotel (~10 min)
4. **Swap the base map style:** Change the tile URL from OSM Standard to CartoDB Positron (~10 min)
5. **Add your data:** Replace the sample GeoJSON path with one of your real POI files. See your actual data appear on the map! (~20 min)
6. **Customize a popup:** Find the popup template and modify what information appears when you click a marker (~20 min)
7. **Test on your phone:** Open the file via a local server or push to GitHub Pages and check mobile layout (~15 min)

### Deliverable
- The starter template loads your real POI data from at least 2 category files
- You've customized the popup to show Chinese name, category, and description
- You've tested on a phone browser

### Self-Check
- [ ] I can explain what tiles are and why maps load in squares
- [ ] I can change the map's center point and zoom level
- [ ] I successfully loaded real GeoJSON data onto the web map
- [ ] I modified a popup template to show different information

---

## Module 5b -- Building Features & Deploying (Phase 3, Week 6-7)

**Estimated time: 3-4 hours**

Now that you understand the starter template, add features and deploy the live map.

### Concepts
- Layer groups and layer controls in Leaflet.js
- Styling GeoJSON features (custom icons, colored lines)
- Making web pages responsive for mobile screens
- Deploying a static site to GitHub Pages

### Hands-On (~3 hours)
1. **Load all POI categories:** Add all 7+ category GeoJSON files as separate layer groups (~30 min)
2. **Add layer toggle controls:** Use `L.control.layers` to let users show/hide categories (~30 min)
3. **Add day filter:** Create buttons or a dropdown that shows only POIs for a selected day (~30 min)
4. **Add route lines:** Load the daily route GeoJSON files and display them as colored lines (~20 min)
5. **Custom icons:** Use different colored markers for each category (Leaflet `L.divIcon` or icon images) (~30 min)
6. **Mobile polish:** Test on phones, adjust popup width, increase touch targets (~20 min)
7. **Deploy to GitHub Pages:** Push to GitHub, enable Pages in repo Settings, verify the live URL works (~20 min)

### Deliverable
- Working web map with all categories, layer toggles, and day filter
- Deployed at `https://<username>.github.io/shanghai-trip-gis/`
- Works on mobile phones

### Self-Check
- [ ] I can add a new data layer to the map by loading a GeoJSON file
- [ ] Layer toggle controls work (show/hide categories)
- [ ] The map is deployed and accessible via a public URL
- [ ] The map works on a phone screen

---

## Module 6 -- Cartographic Design (Phase 4, Week 7-8)

**Estimated time: 2-3 hours**

### Concepts
- Map design principles: hierarchy, contrast, simplicity
- Color theory for maps (colorblind-friendly palettes)
- Typography on maps (labels, annotations)
- Legend design
- The difference between a "map" and a "good map"

### Hands-On (~2 hours)
1. Review the web map critically: What's cluttered? What's hard to read? (~15 min)
2. Apply a consistent color palette (use [ColorBrewer](https://colorbrewer2.org/)) (~20 min)
3. Design a clean legend for the web map (~20 min)
4. Improve popups -- is the most important info (Chinese name!) prominent enough? (~20 min)
5. Export a "hero image" of the full map from QGIS for portfolio use (~30 min)
   - Use the print layout skills from Module 4
   - Design a polished composition with title, legend, and attribution

### Deliverable
- Polished web map with intentional design choices
- One QGIS print layout exported as PNG/PDF (portfolio hero image)
- Each member can explain one design decision they made and why

### Self-Check
- [ ] I can name 3 principles of good map design
- [ ] I chose a colorblind-friendly palette and can explain why
- [ ] The Chinese name is the most prominent text in each popup
- [ ] I exported a portfolio-quality map image from QGIS

---

## Module 7 -- Story Map (Phase 6, Post-Trip)

**Estimated time: 2-3 hours**

A **story map** combines maps with narrative text and photos to tell the story of your trip. We provide a template -- your job is to fill it with your content.

### Concepts
- Story maps as a GIS communication tool
- Geotagged photography -- photos with embedded location data
- Narrative cartography -- using maps to tell stories, not just show data
- Portfolio presentation -- framing your work for an audience

### Hands-On (~2 hours)
1. **Gather content:** Collect your best photos, GPS traces, and trip notes from each day (~30 min)
2. **Open the story template:** Open `web/story-template.html` and read the placeholder sections (~10 min)
3. **Fill in each day:** Replace placeholder text and photo paths with your real content (~45 min)
4. **Add actual routes:** If you recorded GPS traces, add them as "actual route" layers alongside the planned routes (~20 min)
5. **Write a reflection:** Add a closing section connecting what you learned to your field of study (~15 min)

### Optional: Sustainability Reflection
For the team member focused on sustainability:
- Compare planned vs. actual transport modes -- did you walk more or less than planned?
- Reflect on sustainable tourism observations from the trip
- Connect findings to SDG 11 (Sustainable Cities) or SDG 12 (Responsible Consumption)

### Deliverable
- Completed story map with photos, notes, and real trip data
- Project reflection in README.md
- Portfolio-ready screenshots

### Self-Check
- [ ] Each day of the trip has at least one photo and a short narrative
- [ ] The story map loads and scrolls correctly
- [ ] I wrote a reflection connecting GIS to my field of study
- [ ] I have at least one portfolio-quality screenshot of the final map

---

## Skills Matrix

By the end of this project, each member will have practiced:

| Skill | Module | Tool Used |
|-------|--------|-----------|
| Understanding GIS concepts | 1 | Discussion |
| Reading coordinates | 2 | Google Maps, geojson.io |
| Creating spatial data | 3 | geojson.io, text editor |
| Using desktop GIS software | 4 | QGIS |
| Performing spatial analysis | 4 | QGIS |
| Creating print maps for offline use | 4 | QGIS Print Layout |
| Reading and customizing web maps | 5a | Leaflet.js, HTML/CSS/JS |
| Building and deploying web maps | 5b | Leaflet.js, GitHub Pages |
| Cartographic design | 6 | QGIS, Leaflet.js |
| Version control & collaboration | All | Git, GitHub Desktop |
| Real-world data collection | Trip | Phone GPS, camera |
| Storytelling with maps | 7 | Story map template |
