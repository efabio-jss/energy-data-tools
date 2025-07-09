import os
import re
import utm
import zipfile
import requests
import pandas as pd
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
from tabula import read_pdf

# === Output directory (edit as needed) ===
download_dir = "output/spain_grid_data"
os.makedirs(download_dir, exist_ok=True)

# === Source URLs (replace with updated links if needed) ===
urls = {
    "REE": "https://www.ree.es/es/clientes/generador/acesso-conexion/conoce-la-capacidade-de-acesso",
    "e-distribucion": "https://www.edistribucion.com/es/red-electrica/Nodos_capacidad_acesso.html",
    "e-redes": "https://www.eredesdistribucion.es/mapa-interactivo-de-la-red",
    "i-de": "https://www.i-de.es/conexion-red-electrica/produccion-energia/mapa-capacidade-acesso",
    "naturgy": "https://estaticos.naturgy.com/ufd/capacidades/publicacion%20capacidade.pdf",
    "viesgo": "https://www.viesgodistribucion.com/mapa-interactivo-de-la-red"
}

def download_file(url, download_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        filename = Path(urlparse(url).path).name or f"file_{datetime.now().timestamp()}.pdf"
        file_path = os.path.join(download_path, filename)
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"✅ Saved: {file_path}")
    except Exception as e:
        print(f"❌ Failed to download {url}: {e}")

def download_all_files():
    print(f"📥 Downloading data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    for name, url in urls.items():
        print(f"➡️ {name}")
        download_file(url, download_dir)

def detectar_tipo_coordenada(x, y):
    if 100000 < x < 1000000 and 4000000 < y < 5000000:
        return "UTM (ETRS89)"
    elif -90 <= x <= 90 and -180 <= y <= 180:
        return "Lat/Lon"
    else:
        return "Unknown"

def converter_utm_para_latlon(x, y, zona=30, hemisferio='N'):
    try:
        lat, lon = utm.to_latlon(x, y, zona, northern=(hemisferio.upper() == 'N'))
        return lat, lon
    except:
        return None, None

def formatar_dataframe(df):
    colunas = df.columns.str.upper()
    if 'X' in colunas and 'Y' in colunas:
        df.columns = [c.upper() for c in df.columns]
        df[['Latitude', 'Longitude']] = df.apply(
            lambda row: pd.Series(converter_utm_para_latlon(row['X'], row['Y'])), axis=1
        )
    elif 'LATITUDE' in colunas and 'LONGITUDE' in colunas:
        pass
    else:
        df['Latitude'] = None
        df['Longitude'] = None

    df_formatado = pd.DataFrame()
    df_formatado['Region'] = df.get('REGION', None)
    df_formatado['Substation'] = df.get('SUBESTACION', df.get('SUBSTATION', None))
    df_formatado['Available Capacity MW'] = df.get('AVAILABLE CAPACITY MW', df.get('CAPACIDAD DISPONIBLE (MW)', None))
    df_formatado['Latitude'] = df['Latitude']
    df_formatado['Longitude'] = df['Longitude']
    df_formatado['Grid Type'] = df.get('GRID TYPE', None)
    df_formatado['Grid Owner'] = df.get('GRID OWNER', None)
    return df_formatado

def gerar_kmz(df, output_path):
    kml = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document><name>Substations</name>"""
    for _, row in df.iterrows():
        if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
            desc = (
                f"Substation: {row['Substation']}<br/>"
                f"Available Capacity: {row['Available Capacity MW']} MW<br/>"
                f"Grid Type: {row['Grid Type']}<br/>"
                f"Grid Owner: {row['Grid Owner']}"
            )
            kml += f"""
    <Placemark>
      <name>{row['Substation']}</name>
      <description>{desc}</description>
      <Point><coordinates>{row['Longitude']},{row['Latitude']},0</coordinates></Point>
    </Placemark>"""
    kml += "\n</Document></kml>"

    kml_file = output_path.replace('.kmz', '.kml')
    with open(kml_file, 'w', encoding='utf-8') as f:
        f.write(kml)
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as kmz:
        kmz.write(kml_file, arcname='doc.kml')

# === Main ===
if __name__ == "__main__":
    download_all_files()

    df_final = pd.DataFrame()
    pdf_files = [f for f in os.listdir(download_dir) if f.lower().endswith('.pdf')]
    for pdf in pdf_files:
        pdf_path = os.path.join(download_dir, pdf)
        try:
            print(f"🔎 Processing: {pdf}")
            tables = read_pdf(pdf_path, pages='all', multiple_tables=True, lattice=True)
            if not tables:
                print(f"⚠️ No tables extracted from {pdf}")
                continue
            df = pd.concat(tables, ignore_index=True)
            df_formatado = formatar_dataframe(df)
            df_formatado['Source'] = pdf
            df_final = pd.concat([df_final, df_formatado], ignore_index=True)
        except Exception as e:
            print(f"❌ Error processing {pdf}: {e}")

    # Save Excel
    excel_output_path = os.path.join(download_dir, "Substations_Unificado.xlsx")
    df_final.to_excel(excel_output_path, index=False)
    print(f"✅ Excel saved: {excel_output_path}")

    # Save KMZ
    kmz_output_path = os.path.join(download_dir, "Substations_Unificado.kmz")
    gerar_kmz(df_final, kmz_output_path)
    print(f"📍 KMZ saved: {kmz_output_path}")
