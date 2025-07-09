# ⚡ Portugal Electricity Consumption Visualizer

A Python-based tool that retrieves electricity consumption data from the **E-REDES Open Data API** and enables interactive filtering and chart generation for any region in Portugal.

---

## ✅ Features

- Connects to the official public dataset:
  - `https://e-redes.opendatasoft.com/api/records/1.0/search/`
- Filters by:
  - District (`distrito`)
  - Municipality (`concelho`)
  - Parish (`freguesia`)
  - Year(s)
- Aggregates data by selected administrative level
- Converts values from kWh to GWh
- Visualizes results using `matplotlib` as grouped bar charts

---

## 📥 Inputs (via terminal)

- District (optional)
- Municipality (optional)
- Parish (optional)
- One or more years (e.g., `2022,2023`)
- Aggregation level: `distrito`, `concelho`, or `freguesia`

---

## 📊 Output

- A grouped bar chart showing electricity consumption in GWh.
- Each group is based on the selected geographic level.
- Each color represents a year.

---

## ⚙️ How It Works

1. Builds an API query for each selected year.
2. Retrieves and filters results by location and year.
3. Converts values from kWh to GWh.
4. Aggregates by level (district, municipality, or parish).
5. Visualizes using Matplotlib.

---

## 🔐 Requirements

- Python 3.x
- Install dependencies:
```bash
pip install pandas requests matplotlib numpy

🧠 Use Cases
Municipal planning and infrastructure development

Energy consumption trend analysis

Academic or policy research

Support for renewable energy deployment studies


🇵🇹 Instantly Explore Portugal's Power Usage by Region!

