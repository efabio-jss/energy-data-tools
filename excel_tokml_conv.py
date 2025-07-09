import pandas as pd
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString
import os

# 🔧 Defina o caminho dos ficheiros (pode ser ajustado conforme necessário)
base_path = "data"
os.makedirs(base_path, exist_ok=True)

excel_file = os.path.join(base_path, "your_input_file.xlsx")  # Substitua com o nome real do ficheiro
kml_file = os.path.join(base_path, "output.kml")

# 📥 Carregar o Excel
df = pd.read_excel(excel_file)

# 🌍 Criar a estrutura base do KML
kml = Element('kml', xmlns="http://www.opengis.net/kml/2.2")
document = SubElement(kml, 'Document')

# 🏷️ Adicionar placemarks
for _, row in df.iterrows():
    placemark = SubElement(document, 'Placemark')
    
    name = SubElement(placemark, 'name')
    name.text = str(row['Project Name'])

    description = SubElement(placemark, 'description')
    description.text = (
        f"Capacity: {row['Capacity (MW)']} MW\n"
        f"Status: {row['Status']}\n"
        f"Owner: {row['Owner'] if pd.notna(row['Owner']) else 'Unknown'}\n"
        f"Location Accuracy: {row['Location accuracy']}"
    )

    point = SubElement(placemark, 'Point')
    coordinates = SubElement(point, 'coordinates')
    coordinates.text = f"{row['Longitude']},{row['Latitude']},0"

# 💾 Salvar como ficheiro .kml formatado
kml_str = parseString(tostring(kml)).toprettyxml(indent="  ")

with open(kml_file, "w", encoding="utf-8") as f:
    f.write(kml_str)

print(f"KML file successfully generated: {kml_file}")
