# ☀️ Portugal Renewable Production Capacity Extractor

This Python script connects to the **E-REDES Open Data API** and retrieves solar PV production data (connection capacity) at the municipal level in Portugal. It allows optional filtering and exports to Excel.

---

## ✅ Features

- Connects to the dataset:
  - `25-plr-producao-renovavel`
- Optional filtering by municipality (`concelho`)
- Returns:
  - Municipality
  - Year
  - Installed Capacity (kW)
- Displays results in terminal
- Optionally saves results to Excel

---

## 📥 User Inputs

Prompted through terminal:
- Municipality (optional)
- Whether to save the result to Excel

---

## 💾 Output

If saved, results will be written to:
renewable_capacity_results.xlsx


---

## ⚙️ How It Works

1. Prompts for municipality filter.
2. Builds an API request.
3. Processes the response into a Pandas DataFrame.
4. Displays the results.
5. Saves to Excel if requested.

---

## 🔐 Requirements

- Python 3.x
- Install dependencies:
```bash
pip install pandas requests openpyxl


🧠 Use Cases
Analyze solar PV growth by municipality

Support renewable energy project development

Track regional trends in installed capacity

