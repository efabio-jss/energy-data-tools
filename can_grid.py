import requests
import simplekml
import zipfile
import json
import os

# Diretório de saída (pode ser modificado conforme necessário)
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

geojson_projects = os.path.join(output_dir, "projects_data.geojson")
geojson_lines = os.path.join(output_dir, "transmission_lines_data.geojson")
kml_file = os.path.join(output_dir, "canada_grid.kml")
kmz_file = os.path.join(output_dir, "canada_grid.kmz")

# URLs das camadas do ArcGIS Online
urls = {
    "projects": "https://services5.arcgis.com/6czaFAhUmpKiwuMe/arcgis/rest/services/Projects_Upload/FeatureServer/0/query",
    "transmission_lines": "https://services5.arcgis.com/6czaFAhUmpKiwuMe/arcgis/rest/services/AIES_Transmission_Lines_View_Layer/FeatureServer/0/query"
}

# Parâmetros para obter os dados em formato GeoJSON
params = {"where": "1=1", "outFields": "*", "f": "geojson"}

def download_data(url, filepath):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(response.json(), f, indent=4)
        print(f"✅ Data saved: {filepath}")
    else:
        print(f"❌ Error fetching data: {response.status_code}")

# Baixar dados
download_data(urls["projects"], geojson_projects)
download_data(urls["transmission_lines"], geojson_lines)

# Criar novo KML
kml = simplekml.Kml()

def detect_voltage_field(geojson_file):
    with open(geojson_file, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)
    if "features" in geojson_data and geojson_data["features"]:
        props = geojson_data["features"][0]["properties"]
        for key in props:
            if "voltage" in key.lower():
                return key
    return None

voltage_field = detect_voltage_field(geojson_lines)

def add_features_to_kml(geojson_file, layer_type):
    with open(geojson_file, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

    for feature in geojson_data["features"]:
        if not feature["geometry"]:
            print("⚠️ Warning: Feature without geometry ignored.")
            continue

        coords = feature["geometry"]["coordinates"]
        props = feature["properties"]
        
        if layer_type == "projects":
            name = props.get("Project_Na", "Unnamed")
            description = (
                f"🔋 Name: {name}\n"
                f"⚡ Generator Type: {props.get('Generator_Type', 'Unknown')}\n"
                f"💡 MW Type: {props.get('MW_Type', 'Unknown')}\n"
                f"📊 Status: {props.get('Status_1', 'Unknown')}"
            )
        else:
            name = props.get("NAME", "Unnamed")
            description = (
                f"🔌 Line Name: {name}\n"
                f"⚡ Voltage: {props.get(voltage_field, 'Unknown')}\n"
                f"🏭 TFO: {props.get('TFO', 'Unknown')}"
            )

        geom_type = feature["geometry"]["type"]
        if geom_type == "Point":
            pnt = kml.newpoint(name=name, coords=[(coords[0], coords[1])])
            pnt.description = description
        elif geom_type == "LineString":
            line = kml.newlinestring(name=name, coords=coords)
            line.description = description
        elif geom_type == "Polygon":
            pol = kml.newpolygon(name=name, outerboundaryis=coords[0])
            pol.description = description

add_features_to_kml(geojson_projects, "projects")
add_features_to_kml(geojson_lines, "transmission_lines")

kml.save(kml_file)
print(f"✅ KML file saved: {kml_file}")

with zipfile.ZipFile(kmz_file, "w", zipfile.ZIP_DEFLATED) as kmz:
    kmz.write(kml_file, os.path.basename(kml_file))

os.remove(kml_file)
print(f"🎯 KMZ file generated: {kmz_file}")
