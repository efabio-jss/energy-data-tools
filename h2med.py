from pykml.factory import KML_ElementMaker as KML
from lxml import etree

# Coordenadas dos corredores de hidrogénio
portuguese_hydrogen_backbone = [
    ("Lisboa", (38.7169, -9.1399)),
    ("Leiria", (39.7436, -8.8070)),
    ("Coimbra", (40.2033, -8.4103)),
    ("Porto", (41.1496, -8.6109)),
    ("Braga", (41.5503, -8.4201))
]

spanish_hydrogen_backbone = [
    ("Sevilha", (37.3891, -5.9845)),
    ("Madrid", (40.4168, -3.7038)),
    ("Zaragoza", (41.6488, -0.8891)),
    ("Valência", (39.4699, -0.3763)),
    ("Barcelona", (41.3851, 2.1734))
]

celza_corridor = [
    ("Celorico da Beira", (40.6374, -7.3895)),
    ("Zamora", (41.5033, -5.7446))
]

barmar_corridor = [
    ("Barcelona", (41.3851, 2.1734)),
    ("Marseille", (43.2965, 5.3698))
]

france_germany_link = [
    ("Paris", (48.8566, 2.3522)),
    ("Strasbourg", (48.5734, 7.7521)),
    ("Frankfurt", (50.1109, 8.6821)),
    ("Stuttgart", (48.7758, 9.1829))
]

# Criar o documento KML com estilos
doc = KML.kml(
    KML.Document(
        KML.Style(KML.LineStyle(KML.color("ff00ffff"), KML.width(3)), id="portugal-style"),
        KML.Style(KML.LineStyle(KML.color("ff0000ff"), KML.width(3)), id="spain-style"),
        KML.Style(KML.LineStyle(KML.color("ff00ff00"), KML.width(3)), id="celza-style"),
        KML.Style(KML.LineStyle(KML.color("ff00ff00"), KML.width(3)), id="barmar-style"),
        KML.Style(KML.LineStyle(KML.color("ffff00ff"), KML.width(3)), id="france-germany-style"),
    )
)

# Adicionar cada trajeto como placemark
for path, style_id, name in [
    (portuguese_hydrogen_backbone, "#portugal-style", "Portuguese Hydrogen Backbone"),
    (spanish_hydrogen_backbone, "#spain-style", "Spanish Hydrogen Backbone"),
    (celza_corridor, "#celza-style", "CelZa"),
    (barmar_corridor, "#barmar-style", "BarMar"),
    (france_germany_link, "#france-germany-style", "France-Germany Hydrogen Link")
]:
    line_coords = " ".join(f"{lon},{lat},0" for _, (lat, lon) in path)
    doc.Document.append(
        KML.Placemark(
            KML.name(f"Pipeline {name}"),
            KML.styleUrl(style_id),
            KML.LineString(KML.coordinates(line_coords)),
        )
    )

# Guardar o ficheiro
output_path = "h2med_routes.kml"  # Defina o caminho desejado
with open(output_path, "wb") as f:
    f.write(etree.tostring(doc, pretty_print=True, xml_declaration=True, encoding="UTF-8"))

print(f"KML file successfully generated: {output_path}")
