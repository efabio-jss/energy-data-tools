# EMAP to KMZ Converter

This Python script (`geo.py`)  converts European gas infrastructure data from GeoJSON (EMAP/SciGRID format) into a KMZ file suitable for visualization in Google Earth.  
The script aggregates data from pipelines, nodes, production units, and storage facilities, enriching each feature with relevant metadata.

---

## 🗂️ Features

The `geo.py` script:

- Loads `.geojson` files describing the European gas network;
- Automatically classifies each `Node` as one of the following:
  - `Storage`, `Production`, `Entry Point`, `Exit Point`, `LNG Terminal`, `Compressor Station`, etc.;
- Extracts metadata from the `param` and `method` fields (e.g., elevation, status, commissioning year);
- Generates a `.kmz` file structured for interactive exploration in Google Earth;
- Applies distinctive icons based on inferred node type;
- Includes detailed popup descriptions for each feature, such as:
  - ID
  - Name
  - Country
  - Inferred type
  - Technical parameters
  - Data origin and attribution method

---

## 📦 Requirements

Make sure the following Python packages are installed:

```bash
pip install geopandas simplekml
📁 Expected File Structure
The script expects the following .geojson files to be present in the same directory as geo.py:

EMAP_Raw_Nodes.geojson

EMAP_Raw_PipeSegments.geojson

EMAP_Raw_Productions.geojson

EMAP_Raw_Storages.geojson

🚀 Usage
Place all .geojson files and geo.py in the same folder.

Adjust the folder_path in the script if needed.

Run the script:

bash
Copy
Edit
python geo.py
The file infraestrutura_gas_estilizado.kmz will be generated in the same folder and can be opened in Google Earth.

🧠 Technical Notes
Fields such as status, commissioning_year, and decommissioning_year are extracted when available and included in the KMZ description.

Node types are inferred based on keywords in the name field.

The attribution method make_Attrib(const) indicates that the value was set as a constant during dataset generation — it does not imply the infrastructure is physically constructed.

📌 Data Source
Based on the SciGRID_gas EMAP dataset and visual references from ENTSOG/GIE system capacity maps.

🔒 License
See the LICENSE file included with the original dataset for data licensing.

🙏 Acknowledgments
This tool was developed with support from Universal Kraft for analysis and visualization of European gas infrastructure.