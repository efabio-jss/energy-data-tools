import argparse, json, math, os, re, sys, unicodedata, zipfile
from pathlib import Path
from typing import Optional
import pandas as pd
import requests

API_V21 = "https://e-redes.opendatasoft.com/api/explore/v2.1/catalog/datasets/capacidade-rececao-rnd/records"

def strip_accents(s: str) -> str:
    return "".join(ch for ch in unicodedata.normalize("NFD", s) if unicodedata.category(ch) != "Mn")

def norm_name(s: Optional[str]) -> str:
    if s is None: return ""
    s = str(s)
    s = re.sub(r"\([^)]*\)", " ", s)        # remove ( ... )
    s = strip_accents(s).upper()
    s = re.sub(r"[^A-Z0-9 ]+", " ", s)      # pontuação -> espaço
    return " ".join(s.split())

def to_float_maybe(x):
    if x is None: return None
    if isinstance(x, (int, float)) and not (isinstance(x, float) and math.isnan(x)):
        return float(x)
    s = str(x).strip()
    if s == "": return None
    s = s.replace(",", ".")
    try:
        return float(s)
    except:
        m = re.search(r"[-+]?\d+(?:[.,]\d+)?", s)
        if m:
            try: return float(m.group(0).replace(",", "."))
            except: return None
    return None

def parse_coord(coord_text, is_lon=False) -> Optional[float]:
    if coord_text is None: return None
    s = str(coord_text).strip()
    if s == "": return None
    # decimal simples
    dec_try = to_float_maybe(s)
    if dec_try is not None and not any(ch in s for ch in ("°","º","'","’","′","\"","”","″","N","S","E","W","n","s","e","w")):
        if is_lon and dec_try > 0: dec_try = -dec_try  # Portugal a Oeste
        return dec_try
    # DMS
    s = s.replace("º","°").replace("’","'").replace("′","'").replace("”",'"').replace("″",'"')
    m = re.search(r"""(?ix)
        (?P<deg>[-+]?\d+(?:[.,]\d+)?)\s*(?:°)?
        \s*(?P<min>\d+(?:[.,]\d+)?)?\s*(?:')?
        \s*(?P<sec>\d+(?:[.,]\d+)?)?\s*(?:")?
        \s*(?P<hem>[NSEW])?
    """, s)
    if not m: return None
    deg = float((m.group("deg") or "0").replace(",", "."))
    minutes = float((m.group("min") or "0").replace(",", "."))
    seconds = float((m.group("sec") or "0").replace(",", "."))
    hem = (m.group("hem") or "").upper()
    val = abs(deg) + minutes/60.0 + seconds/3600.0
    if hem in ("S","W"): val = -val
    elif hem in ("N","E"): pass
    else:
        if str(coord_text).strip().startswith("-") or str(deg).startswith("-"):
            val = -val
        elif is_lon and val > 0:
            val = -val
    return val

# ---------- API ----------
def fetch_all_records(instalacao: Optional[str]=None, limit:int=1000) -> pd.DataFrame:
    rows, offset = [], 0
    where = f"instalacao='{instalacao}'" if instalacao else None
    while True:
        params = {"limit": limit, "offset": offset, "order_by": "instalacao"}
        if where: params["where"] = where
        r = requests.get(API_V21, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        results = data.get("results", [])
        if not results: break
        rows.extend(results); offset += limit
        if len(results) < limit: break
    return pd.DataFrame(rows)

# ---------- column detection ----------
def pick_col(cols, *cands):
    low = {c.lower(): c for c in cols}
    for k in cands:
        if k.lower() in low: return low[k.lower()]
    for k in cands:
        for c in cols:
            if k.lower() in c.lower(): return c
    return None

def detect_api_fields(df):
    name = pick_col(df.columns, "instalacao","substation","nome","designacao","station","installation")
    muni = pick_col(df.columns, "municipio","municipality","concelho")
    dist = pick_col(df.columns, "distrito","district")
    cap  = pick_col(df.columns, "capacity","capacidade")
    av   = pick_col(df.columns, "available_capacity","capacidade_disponivel","capacidade disponivel","available")
    return name, muni, dist, cap, av

def detect_excel_fields(df):
    sub = pick_col(df.columns, "Substation","Subestacao","Subestação")
    muni= pick_col(df.columns, "Municipality","Municipio","Município","Concelho")
    dist= pick_col(df.columns, "District","Distrito")
    cap = pick_col(df.columns, "Capacity","Capacidade")
    av  = pick_col(df.columns, "Available Capacity","Capacidade Disponivel","Capacidade Disponível","Available")
    lat = pick_col(df.columns, "Latitude","Lat")
    lon = pick_col(df.columns, "Longitude","Lon")
    return sub, muni, dist, cap, av, lat, lon

# ---------- KMZ ----------
def build_kmz(df: pd.DataFrame, sub_col, av_col, lat_col, lon_col,
              icon_on: Path, icon_off: Path, out_kmz: Path):
    kml_header = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2"><Document>
  <name>PT SUBS</name>
  <Style id="onStyle"><IconStyle><scale>1.2</scale><Icon><href>ON.png</href></Icon></IconStyle><LabelStyle><scale>1.1</scale></LabelStyle></Style>
  <Style id="offStyle"><IconStyle><scale>1.2</scale><Icon><href>off.png</href></Icon></IconStyle><LabelStyle><scale>1.1</scale></LabelStyle></Style>
"""
    kml_footer = "</Document></kml>\n"
    placemarks = []
    for _, r in df.iterrows():
        lat = parse_coord(r[lat_col], is_lon=False)
        lon = parse_coord(r[lon_col], is_lon=True)
        if lat is None or lon is None: continue
        av  = to_float_maybe(r[av_col]) or 0.0
        style = "#onStyle" if av > 0 else "#offStyle"
        sub = str(r[sub_col])
        desc = f"<b>Substation:</b> {sub}<br/><b>Available Capacity:</b> {r[av_col]}<br/><b>Latitude:</b> {lat:.6f}<br/><b>Longitude:</b> {lon:.6f}"
        placemarks.append(
            f"<Placemark><name>{sub}</name><styleUrl>{style}</styleUrl>"
            f"<description><![CDATA[{desc}]]></description>"
            f"<Point><coordinates>{lon:.8f},{lat:.8f},0</coordinates></Point></Placemark>"
        )
    kml = kml_header + "\n".join(placemarks) + kml_footer
    with zipfile.ZipFile(out_kmz, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("doc.kml", kml.encode("utf-8"))
        if icon_on.exists():  z.write(str(icon_on), arcname="ON.png")
        if icon_off.exists(): z.write(str(icon_off), arcname="of.png")

# ---------- main ----------
def main():
    ap = argparse.ArgumentParser(description="Atualiza Capacity/Available e gera CSVs + KMZ.")
    ap.add_argument("--excel", required=True, help="Caminho para PT SUBS FINAL.xlsx")
    ap.add_argument("--instalacao", default=None, help="Filtrar por instalação exata (opcional)")
    ap.add_argument("--icons_on", default="ON.png", help="PNG para Available>0")
    ap.add_argument("--icons_off", default="of.png", help="PNG para Available=0")
    ap.add_argument("--kmz_out", default="PT_SUBS.kmz", help="Ficheiro KMZ de saída")
    ap.add_argument("--csv_dir", default=None, help="Pasta para guardar CSVs (por omissão, ao lado do Excel)")
    ap.add_argument("--backup", action="store_true", help="Guardar backup do Excel")
    args = ap.parse_args()

    xls_path = Path(args.excel).expanduser().resolve()
    if not xls_path.exists():
        print(f"[ERRO] Excel não encontrado: {xls_path}", file=sys.stderr); sys.exit(1)
    csv_dir = Path(args.csv_dir).resolve() if args.csv_dir else xls_path.parent

    print("[1/5] A obter dados da API…")
    df_api = fetch_all_records(args.instalacao)
    if df_api.empty:
        print("[AVISO] API devolveu 0 registos. Nada para atualizar.")
    name_a, muni_a, dist_a, cap_a, av_a = detect_api_fields(df_api)
    if not name_a or not cap_a or not av_a:
        print(f"[ERRO] Colunas da API não detetadas. Encontradas: {list(df_api.columns)}", file=sys.stderr)
        sys.exit(2)

    df_api["_SUB_N"]  = df_api[name_a].map(norm_name)
    df_api["_MUNI_N"] = df_api[muni_a].map(norm_name) if muni_a else ""
    df_api["_DIST_N"] = df_api[dist_a].map(norm_name) if dist_a else ""

    print("[2/5] A carregar Excel…")
    df_x = pd.read_excel(xls_path)
    sub_x, muni_x, dist_x, cap_x, av_x, lat_x, lon_x = detect_excel_fields(df_x)
    for need, nm in [("Substation", sub_x), ("Available Capacity", av_x), ("Capacity", cap_x),
                     ("Municipality", muni_x), ("District", dist_x), ("Latitude", lat_x), ("Longitude", lon_x)]:
        if nm is None:
            print(f"[ERRO] Coluna '{need}' não encontrada no Excel.", file=sys.stderr); sys.exit(3)

    # para CSV "updated_rows": manter cópias do antes
    before_cap = df_x[cap_x].copy()
    before_av  = df_x[av_x].copy()

    df_x["_SUB_N"]  = df_x[sub_x].map(norm_name)
    df_x["_MUNI_N"] = df_x[muni_x].map(norm_name)
    df_x["_DIST_N"] = df_x[dist_x].map(norm_name)

    print("[3/5] A cruzar…")
    api_min = df_api[["_SUB_N","_MUNI_N","_DIST_N", cap_a, av_a]].copy()
    m1 = df_x.merge(api_min, how="left", on=["_SUB_N","_MUNI_N","_DIST_N"], suffixes=("","_api"))
    still = m1[cap_a].isna() & m1[av_a].isna()
    if still.any():
        api_by_sub = df_api[["_SUB_N", cap_a, av_a]].drop_duplicates("_SUB_N")
        m1.loc[still, [cap_a, av_a]] = (
            m1.loc[still, ["_SUB_N"]].merge(api_by_sub, how="left", on="_SUB_N")[[cap_a, av_a]].values
        )

    # aplicar updates
    updated_mask = []
    for i in range(len(m1)):
        new_cap = m1.at[i, cap_a]
        new_av  = m1.at[i, av_a]
        changed = False
        if pd.notna(new_cap):
            df_x.at[i, cap_x] = to_float_maybe(new_cap); changed = True
        if pd.notna(new_av):
            df_x.at[i, av_x]  = to_float_maybe(new_av);  changed = True
        updated_mask.append(changed)
    updated_mask = pd.Series(updated_mask)

    # não correspondências (sem dados novos)
    unmatched_mask = m1[cap_a].isna() & m1[av_a].isna()
    unmatched = df_x.loc[unmatched_mask, [sub_x, muni_x, dist_x]].copy()

    # construir CSV de updated_rows (apenas onde houve mudança real)
    def _neq(a, b):
        fa, fb = to_float_maybe(a), to_float_maybe(b)
        if fa is None and fb is None: return False
        if fa is None or fb is None:  return True
        return abs(fa - fb) > 1e-9

    changed_rows_mask = (
        _neq(before_cap, df_x[cap_x]) |
        _neq(before_av,  df_x[av_x])
    )
    # quando _neq recebe Series, devolve escalar - por isso fazemos elemento a elemento:
    changed_rows_mask = [(abs((to_float_maybe(a) or 0) - (to_float_maybe(b) or 0)) > 1e-9)
                         or ((a is None) ^ (b is None))
                         for a, b in zip(before_cap, df_x[cap_x])]
    changed_rows_mask2 = [(abs((to_float_maybe(a) or 0) - (to_float_maybe(b) or 0)) > 1e-9)
                          or ((a is None) ^ (b is None))
                          for a, b in zip(before_av, df_x[av_x])]
    changed_rows_mask = pd.Series([cr or cr2 for cr, cr2 in zip(changed_rows_mask, changed_rows_mask2)])

    updated_rows = pd.DataFrame({
        "Substation": df_x[sub_x],
        "Municipality": df_x[muni_x],
        "District": df_x[dist_x],
        "Capacity_before": before_cap,
        "Capacity_after":  df_x[cap_x],
        "Available_before": before_av,
        "Available_after":  df_x[av_x],
    })[changed_rows_mask].copy()

    print(f"[Resumo] Linhas atualizadas: {len(updated_rows)}")
    print(f"[Resumo] Sem correspondência: {len(unmatched)}")
    if len(unmatched):
        print("[Lista de não correspondências]:")
        for _, r in unmatched.iterrows():
            print(f"  - {r[sub_x]} | {r[muni_x]} | {r[dist_x]}")

    # guardar CSVs
    stem = xls_path.stem
    updated_csv   = csv_dir / f"{stem}_updated_rows.csv"
    unmatched_csv = csv_dir / f"{stem}_unmatched.csv"
    updated_rows.to_csv(updated_csv, index=False)
    unmatched.to_csv(unmatched_csv, index=False)
    print(f"[OK] CSV atualizados: {updated_csv.name}")
    print(f"[OK] CSV não-correspondências: {unmatched_csv.name}")

    # guardar Excel (backup opcional)
    if args.backup:
        bak = xls_path.with_suffix(".backup.xlsx")
        pd.read_excel(xls_path).to_excel(bak, index=False)
        print(f"[OK] Backup criado: {bak.name}")
    # remover colunas auxiliares e escrever
    df_x.drop(columns=["_SUB_N","_MUNI_N","_DIST_N"], inplace=True)
    df_x.to_excel(xls_path, index=False)
    print(f"[OK] Excel atualizado: {xls_path.name}")

    # KMZ
    try:
        build_kmz(
            df_x, sub_x, av_x, lat_x, lon_x,
            icon_on=Path(args.icons_on).resolve(),
            icon_off=Path(args.icons_off).resolve(),
            out_kmz=Path(args.kmz_out).resolve()
        )
        print(f"[OK] KMZ gerado: {args.kmz_out}")
    except Exception as e:
        print(f"[AVISO] Falha ao gerar KMZ: {e}")

if __name__ == "__main__":
    main()
