# 🔋 Hydrogen Backbone KML Generator (H2MED)

This Python script generates a `.kml` file that visualizes the proposed hydrogen pipeline corridors for the **H2MED project**, covering parts of Portugal, Spain, France, and Germany.

---

## ✅ Key Features

- Creates a structured KML with `LineStrings` for each corridor using https://www.h2inframap.eu/#map
- Assigns unique styles (colors) for each route:
  - Portuguese Backbone → Light Blue
  - Spanish Backbone → Dark Blue
  - CelZa & BarMar → Green
  - France-Germany Link → Purple
- Includes named placemarks for easy navigation.
- Output ready for **Google Earth** or GIS platforms.

---

## 🗺️ Route Definitions

Each route is defined by a list of named geographic coordinates (latitude, longitude):

- **Portuguese Backbone**:
  Lisboa → Leiria → Coimbra → Porto → Braga

- **Spanish Backbone**:
  Sevilha → Madrid → Zaragoza → Valência → Barcelona

- **CelZa Corridor**:
  Celorico da Beira → Zamora

- **BarMar Link**:
  Barcelona → Marseille

- **France-Germany Link**:
  Paris → Strasbourg → Frankfurt → Stuttgart

---

## ⚙️ How It Works

1. Each route is defined as a Python list of coordinates.
2. Each route is assigned a color-coded style.
3. The script builds the KML structure with placemarks and coordinates.
4. The KML is written to a file on disk.

---

## 📂 Output

The script produces:

h2med_routes.kml


This file includes:
- Named pipelines
- Styled color-coded lines
- Precise route coordinates

---

## 🔐 Requirements

- Python 3.x
- Install with:
```bash
pip install pykml lxml

🌐 Visualize the H2MED Hydrogen Network with a Click!
