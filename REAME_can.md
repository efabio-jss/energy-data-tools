# 🇨🇦 Canada Grid Mapping – KML/KMZ Generator

🌍 Generate Beautiful Canada Power Maps in Seconds!

This Python tool fetches geospatial data from ArcGIS Online layers related to power generation projects and transmission lines in Canada. It converts the data into a KMZ file, ready to be opened in Google Earth or any GIS platform.

---

## ✅ Features

- Connects to ArcGIS FeatureServer APIs:
  - Projects Layer
  - Transmission Lines Layer
- Downloads both datasets as GeoJSON files.
- Auto-detects voltage fields from transmission line attributes.
- Creates a clean, descriptive KML file with:
  - Points for generation projects
  - Lines for transmission infrastructure
- Converts KML into a KMZ archive.

---

## 🌐 Data Sources

- **Projects Layer**  
  `https://services5.arcgis.com/.../Projects_Upload/FeatureServer/0/query`

- **Transmission Lines Layer**  
  `https://services5.arcgis.com/.../AIES_Transmission_Lines_View_Layer/FeatureServer/0/query`

All data is retrieved in GeoJSON format using:


---

## 🗺️ Output Structure

**Projects**
- Project Name
- Generator Type
- MW Type
- Status

**Transmission Lines**
- Line Name
- Voltage (auto-detected field)
- TFO (Transmission Facility Owner)

---

## 💾 Output

All output files are saved in a local `output/` folder:
- `projects_data.geojson`
- `transmission_lines_data.geojson`
- `canada_grid.kmz` (final file for Google Earth)

---

## ⚙️ How It Works

1. Uses `requests` to query ArcGIS Online layers.
2. Parses and stores GeoJSON files.
3. Detects voltage field dynamically.
4. Builds structured KML.
5. Compresses final KML into KMZ.
6. Deletes temporary KML after compression.

---

## 🔐 Requirements

- Python 3.x
- Install dependencies with:
```bash
pip install requests simplekml
