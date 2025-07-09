import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_consumption_data(distrito=None, concelho=None, freguesia=None, anos=None):
    base_url = "https://e-redes.opendatasoft.com/api/records/1.0/search/"
    params = {
        "dataset": "3-consumos-faturados-por-municipio-ultimos-10-anos",
        "rows": 5000
    }

    if distrito:
        params["refine.distrito"] = distrito
    if concelho:
        params["refine.concelho"] = concelho
    if freguesia:
        params["refine.freguesia"] = freguesia

    records = []
    for ano in anos:
        params["refine.ano"] = str(ano)
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code}\n{response.text}")

        data = response.json().get("records", [])
        for item in data:
            fields = item.get("fields", {})
            records.append({
                "ano": fields.get("ano"),
                "distrito": fields.get("distrito"),
                "concelho": fields.get("concelho"),
                "freguesia": fields.get("freguesia"),
                "energia_ativa_kwh": fields.get("energia_ativa_kwh", 0)
            })

    df = pd.DataFrame(records)
    if df.empty:
        raise ValueError("No data found for the selected filters.")
    return df

def plot_consumption(df, level="distrito", title="Filtered Consumption (GWh)"):
    df["energia_ativa_gwh"] = df["energia_ativa_kwh"] / 1e6
    df_grouped = (
        df.groupby(["ano", level])["energia_ativa_gwh"]
          .sum()
          .reset_index()
          .sort_values(["ano", level])
    )

    categories = df_grouped[level].unique()
    anos = df_grouped["ano"].unique()
    bar_width = 0.2
    x = np.arange(len(categories))

    plt.figure(figsize=(12, 8))
    for i, ano in enumerate(anos):
        valores = df_grouped[df_grouped["ano"] == ano].set_index(level)["energia_ativa_gwh"]
        plt.bar(x + i * bar_width, valores, width=bar_width, label=str(ano))

    plt.title(title, fontsize=14)
    plt.xlabel(level.capitalize(), fontsize=12)
    plt.ylabel("Total Consumption (GWh)", fontsize=12)
    plt.xticks(x + bar_width * (len(anos) - 1) / 2, categories, rotation=45, ha="right")
    plt.legend(title="Year")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("=== Electricity Consumption Viewer ===")
    print("Leave any field blank to skip the filter.")

    distrito = input("District (optional): ").strip() or None
    concelho = input("Municipality (optional): ").strip() or None
    freguesia = input("Parish (optional): ").strip() or None
    years_input = input("Enter years (comma-separated, e.g. 2022,2023): ").strip()

    years = [int(y.strip()) for y in years_input.split(",") if y.strip().isdigit()]
    if not years:
        print("Please provide at least one valid year.")
        exit()

    try:
        df = get_consumption_data(distrito, concelho, freguesia, anos=years)
        level = input("Select aggregation level (distrito, concelho, freguesia): ").strip().lower()
        if level not in ["distrito", "concelho", "freguesia"]:
            raise ValueError("Invalid level. Choose from: distrito, concelho, freguesia.")
        plot_consumption(df, level=level, title=f"Electricity Consumption by {level.capitalize()}")
    except Exception as e:
        print(f"Error: {e}")
