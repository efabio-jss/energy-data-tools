# ⚡ E-REDES Substation Data Extractor

This Python script connects to the **E-REDES Open Data API** to retrieve data about reception capacity from substations across Portugal. It allows optional filtering by substation name and optionally exports results to Excel.

---

## ✅ Key Features

- Connects to:
  - `https://e-redes.opendatasoft.com/api/explore/v2.1/catalog/datasets/capacidade-rececao-rnd/records`
- Optionally filter by installation (`instalacao`)
- Loads results into a Pandas DataFrame
- Interactive option to save results as an Excel file

---

## 📥 User Inputs

- **Substation name (optional):** Leave blank to get all records.
- **Export to Excel?** Confirm via prompt (`y/n`)

---

## 💾 Output

If exported, the file will be saved as:
substation_data.xlsx

It will contain all fields provided by the API.

---

## ⚙️ How It Works

1. Prompts the user for a substation name.
2. Sends a filtered or unfiltered API request.
3. Converts results to a DataFrame.
4. Displays and optionally saves results to Excel.

---

## 🔐 Requirements

- Python 3.x
- Install dependencies:
```bash
pip install pandas requests openpyxl

📌 Notes
By default, the API returns up to 100 records.
For more data, implement pagination or modify query parameters.


🧠 Use Cases
Identify substations and reception capacity across Portugal.
Feed GIS or energy feasibility tools with official substation data.
Support analysis and infrastructure planning.

