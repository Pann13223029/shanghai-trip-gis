# GIS Glossary

Plain-English definitions for terms you'll encounter in this project. Refer back here whenever you hit unfamiliar jargon.

---

| Term | Definition |
|------|-----------|
| **Base map** | The background map layer (streets, buildings, water) that provides geographic context. We use OpenStreetMap tiles. |
| **Buffer** | A zone drawn at a set distance around a feature. E.g., "everything within 500m of the hotel" creates a 500m buffer. |
| **Cartography** | The art and science of making maps. Good cartography makes information clear and beautiful. |
| **Cluster** | A group of features close together geographically. We check clustering to make sure same-day POIs are near each other. |
| **Coordinate** | A pair of numbers (longitude, latitude) that pinpoint a location on Earth. E.g., `[121.47, 31.23]` is central Shanghai. |
| **CRS / Coordinate Reference System** | The system that defines how coordinates map to real locations. We use WGS84 (EPSG:4326). |
| **Feature** | A single geographic object in GeoJSON — a point, line, or polygon with attached properties. |
| **FeatureCollection** | A GeoJSON object containing an array of Features. Each of our `.geojson` files is a FeatureCollection. |
| **GCJ-02** | China's mandatory coordinate offset system ("Mars coordinates"). Shifts WGS84 positions by 200-400m. We avoid it by not using Chinese tile providers. |
| **GeoJSON** | A standard file format for encoding geographic data as JSON. Human-readable and works everywhere. |
| **GIS (Geographic Information System)** | Software and methods for capturing, storing, analyzing, and visualizing geographic data. |
| **GPS** | Global Positioning System — satellites that let your phone determine its WGS84 coordinates. |
| **Layer** | A single dataset displayed on a map. Our map has many layers: one per POI category, one per day route, etc. |
| **Latitude (lat)** | How far north or south of the equator. Shanghai is ~31.23°N. In coordinates, this is the SECOND number in GeoJSON. |
| **Leaflet.js** | A lightweight JavaScript library for interactive web maps. Powers our web map. |
| **LineString** | A GeoJSON geometry type representing a path — a series of connected points. Used for routes. |
| **Longitude (lng)** | How far east or west of the Prime Meridian. Shanghai is ~121.47°E. In coordinates, this is the FIRST number in GeoJSON. |
| **Marker** | An icon placed on a map at a specific coordinate to represent a point of interest. |
| **OpenStreetMap (OSM)** | A free, community-built map of the world. We use OSM tiles as our base map. |
| **Overpass Turbo** | A web tool for querying OpenStreetMap data. Like a search engine for map features. |
| **Point** | A GeoJSON geometry type representing a single location. Used for POIs. |
| **POI (Point of Interest)** | A specific place worth visiting or noting — a restaurant, landmark, park, etc. |
| **Polygon** | A GeoJSON geometry type representing an enclosed area. Used for districts and neighborhoods. |
| **Popup** | The info box that appears when you click a marker on a web map. Shows details like name, description, hours. |
| **Print Layout** | A QGIS tool for designing maps to export as PDF or image. Used for offline backup maps. |
| **Projection** | A method for representing the curved Earth on a flat surface. All projections distort something. |
| **QGIS** | Free, open-source desktop GIS software. We use it for spatial analysis and print map exports. |
| **Raster data** | Geographic data stored as a grid of pixels (like a photo). Satellite imagery is raster. We don't create raster data. |
| **Service worker** | A script that runs in the browser to cache files for offline use. Lets our web map work without internet. |
| **Spatial analysis** | Using geographic relationships (distance, overlap, proximity) to answer questions and make decisions. |
| **Spatial join** | Combining two datasets based on their geographic relationship. E.g., "which district is each POI in?" |
| **Story map** | A map-based narrative that combines geographic visualization with text, photos, and sequential storytelling. |
| **Tile** | A small square image (usually 256x256 pixels) that forms part of a web map. Maps load tiles on-demand as you pan and zoom. |
| **Vector data** | Geographic data stored as points, lines, and polygons with coordinates. All our data is vector. |
| **WGS84 (EPSG:4326)** | The coordinate system used by GPS, GeoJSON, and most web maps. The global standard. Our project uses this exclusively. |
| **Zoom level** | A number indicating map magnification. Level 0 = whole world. Level 12 = city. Level 16 = street. Level 18 = building. |
