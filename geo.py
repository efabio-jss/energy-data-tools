import geopandas as gpd
import simplekml
import json
import os

folder_path = r""
output_kmz_path = os.path.join(folder_path, "infraestrutura_gas_estilizado.kmz")

layers = {
    "Nodes": os.path.join(folder_path, "EMAP_Raw_Nodes.geojson"),
    "PipeSegments": os.path.join(folder_path, "EMAP_Raw_PipeSegments.geojson"),
    "Productions": os.path.join(folder_path, "EMAP_Raw_Productions.geojson"),
    "Storages": os.path.join(folder_path, "EMAP_Raw_Storages.geojson")
}

# Ícones por tipo
icon_by_type = {
    "Storage": "http://maps.google.com/mapfiles/kml/shapes/library_maps.png",
    "Production": "http://maps.google.com/mapfiles/kml/shapes/police.png",
    "Entry Point": "http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png",
    "Exit Point": "http://maps.google.com/mapfiles/kml/shapes/info-i_maps.png",
    "LNG Terminal": "http://maps.google.com/mapfiles/kml/shapes/ferry.png",
    "Compressor Station": "http://maps.google.com/mapfiles/kml/shapes/mechanic.png",
    "Interconnection Point": "http://maps.google.com/mapfiles/kml/shapes/target.png",
    "Generic Node": "http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png"
}

def infer_node_type(name: str) -> str:
    name = (name or "").lower()
    if "storage" in name:
        return "Storage"
    elif "production" in name:
        return "Production"
    elif "entry" in name:
        return "Entry Point"
    elif "exit" in name:
        return "Exit Point"
    elif "lng" in name:
        return "LNG Terminal"
    elif "compressor" in name:
        return "Compressor Station"
    elif "interconnection" in name:
        return "Interconnection Point"
    else:
        return "Generic Node"

def format_metadata(row):
    lines = []
    name = row.get("name", "")
    node_type = infer_node_type(name)

    if 'id' in row:
        lines.append(f"<b>ID:</b> {row['id']}")
    if 'name' in row:
        lines.append(f"<b>Name:</b> {name}")
    if 'country_code' in row:
        lines.append(f"<b>Country:</b> {row['country_code']}")
    lines.append(f"<b>Type:</b> {node_type}")

    # STATUS & YEARS
    param = row.get("param", {})
    if isinstance(param, dict):
        status = param.get("status")
        if status:
            lines.append(f"<b>Status:</b> {status}")
        com_year = param.get("commissioning_year")
        if com_year:
            lines.append(f"<b>Commissioned:</b> {com_year}")
        decom_year = param.get("decommissioning_year")
        if decom_year:
            lines.append(f"<b>Decommissioned:</b> {decom_year}")

    lines.append("<hr><b>Parameters:</b>")
    if isinstance(param, dict):
        for k, v in param.items():
            if k not in ["status", "commissioning_year", "decommissioning_year"]:
                lines.append(f"&nbsp;&nbsp;{k}: {v}")

    lines.append("<br><b>Method:</b>")
    method = row.get("method", {})
    if isinstance(method, dict):
        for k, v in method.items():
            lines.append(f"&nbsp;&nbsp;{k}: {v}")
    return "<br>".join(lines), node_type

kml = simplekml.Kml()

for layer_name, filepath in layers.items():
    gdf = gpd.read_file(filepath)
    folder = kml.newfolder(name=layer_name)

    for idx, row in gdf.iterrows():
        for key in ['param', 'method']:
            if isinstance(row.get(key), str):
                try:
                    row[key] = json.loads(row[key])
                except:
                    row[key] = {}

        geom = row.geometry
        description, node_type = format_metadata(row)

        if geom.geom_type == "Point":
            p = folder.newpoint(name=row.get("name", f"{layer_name}_{idx}"),
                                coords=[(geom.x, geom.y)])
            p.description = description
            p.style.iconstyle.icon.href = icon_by_type.get(node_type, icon_by_type["Generic Node"])

        elif geom.geom_type == "LineString":
            ls = folder.newlinestring(name=row.get("name", f"{layer_name}_{idx}"),
                                      coords=list(geom.coords))
            ls.description = description
            ls.style.linestyle.color = simplekml.Color.blue
            ls.style.linestyle.width = 3

kml.savekmz(output_kmz_path)
print(f"✅ KMZ com ícones por tipo de node salvo em:\n{output_kmz_path}")
