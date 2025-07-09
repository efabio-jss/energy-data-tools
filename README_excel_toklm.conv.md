# 🌍 Excel to KML Converter for Geospatial Projects

This Python script transforms an Excel file containing **energy project geospatial data** into a KML file for use in **Google Earth** or other GIS platforms.

---

## ✅ Key Features

- Reads project data from an Excel spreadsheet ( https://globalenergymonitor.org/ ) .
- Converts each row into a **KML Placemark**.
- Includes:
  - Project Name
  - Capacity (MW)
  - Status
  - Owner
  - Location Accuracy
  - Latitude & Longitude
- Generates a **well-structured and formatted KML** file.

---

## 📂 Project Structure

your_project_folder/
│
├── excel_tokml_conv.py # This script
├── your_input_file.xlsx # Input Excel file
└── output.kml # Output KML file


Make sure to update the script with your actual Excel file name.

---

## 📊 Excel Format

| Project Name | Capacity (MW) | Status | Owner | Location accuracy | Latitude | Longitude |
|--------------|----------------|--------|--------|-------------------|----------|-----------|

---

## ⚙️ How It Works

1. Loads the Excel file using `pandas`.
2. Iterates through each row to generate a `<Placemark>` with:
   - Title: Project Name
   - Description: Metadata
   - Point geometry: Longitude, Latitude
3. Formats the KML with `xml.dom.minidom`.
4. Saves the `.kml` file for direct use.

---

## 🔐 Requirements

- Python 3.x
- Packages:
```bash
pip install pandas openpyxl


📍 Use Cases
Map energy projects geographically

Share project locations with teams or clients

Import into Google Earth or GIS platforms

Visual inspection and auditing of location data
