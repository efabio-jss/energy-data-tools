# 🇪🇸 Spain Grid Capacity Extractor & Geospatial Converter

This Python tool automates the **download**, **extraction**, **normalization**, and **geospatial conversion** of substation capacity data from Spanish DSOs. It consolidates all sources into an Excel report and a KMZ map for GIS analysis.

---

## ✅ Features

- Downloads PDFs from:
  - REE, e-distribución, e-redes, i-DE, Naturgy, Viesgo
- Extracts tables using `tabula-py`
- Detects coordinate system (UTM or Lat/Lon)
- Converts UTM to Latitude/Longitude using `utm`
- Exports:
  - `Substations_Unificado.xlsx`
  - `Substations_Unificado.kmz` (Google Earth)

---

## 🗂️ Output Location

Default:
output/spain_grid_data/


Includes:
- All downloaded PDFs
- Consolidated Excel and KMZ files

---

## ⚙️ How It Works

1. Downloads capacity data from each provider.
2. Extracts tabular data using `read_pdf()` from `tabula-py`.
3. Converts and normalizes coordinate systems.
4. Outputs consolidated Excel and KML/KMZ files.

---

## 🔐 Requirements

- Java (for Tabula)
- Python 3.x
- Install dependencies:
```bash
pip install pandas requests utm tabula-py openpyxl


📌 Notes
Java must be installed and available in your system's PATH
KMZ is built from scratch using basic KML structure


🧠 Use Cases
Evaluate grid capacity for solar, wind or storage projects
Create unified grid maps from fragmented Data
Track infrastructure evolution and capacity changes