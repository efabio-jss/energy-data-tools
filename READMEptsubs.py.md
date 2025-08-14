PT Substations Updater & KMZ Generator

Fetch current reception capacity from E-Redes’ open data API, update your Excel workbook, export audit CSVs, and generate a Google Earth KMZ with custom ON/OFF icons based on Available Capacity.

Script: ptsubs_plus_v2.py
Data source (public): E-Redes / Opendatasoft dataset capacidade-rececao-rnd

____________________________________________________________________________________________________________________________________________________________________

What it does:

Downloads records from E-Redes (with pagination).

Normalizes & matches your rows by Substation + Municipality + District
(ignores accents, case, punctuation, and parenthesis content).

Updates the Excel columns Capacity and Available Capacity where a match is found.

Reports unmatched rows (count + list) to the terminal and writes them to CSV.

Exports CSV with before/after values for all rows that changed.

Generates a KMZ:

uses ON.png for Available Capacity > 0

uses of.png for Available Capacity == 0

converts Latitude/Longitude in DMS to decimal degrees if needed

placemark name = Substation; balloon shows Substation, Available Capacity, coordinates.

____________________________________________________________________________________________________________________________________________________________________

Requirements:

Python 3.9+

Packages:

pandas

requests

openpyxl (Excel I/O)

____________________________________________________________________________________________________________________________________________________________________

Outputs:

Excel updated in place (with optional --backup).

CSV audit files (in --csv_dir or next to the Excel):

PT SUBS FINAL_updated_rows.csv
Columns: Substation, Municipality, District, Capacity_before, Capacity_after, Available_before, Available_after.

PT SUBS FINAL_unmatched.csv
Rows that did not match any API record.

KMZ (default PT_SUBS.kmz):

placemark name: Substation

balloon shows Substation, Available Capacity, decimal Latitude, decimal Longitude

icon: ON.png if Available > 0; of.png otherwise

includes the PNGs inside the KMZ, so the file is self-contained.

____________________________________________________________________________________________________________________________________________________________________

Coordinates

Accepts decimal or DMS (e.g., 38° 46' 45.44" N, 9° 06' 08" W).

Longitude without hemisphere is assumed West (negative) for Portugal.

KMZ writes coordinates in decimal.

Console report

At the end you’ll see:

number of updated rows

number of unmatched rows

printed list of unmatched as Substation | Municipality | District

____________________________________________________________________________________________________________________________________________________________________

Data source

E-Redes / Opendatasoft: dataset capacidade-rececao-rnd (public).
The script uses the v2.1 Explore API and paginates (limit/offset) to fetch all records.
