import requests
import pandas as pd

API_URL = "https://e-redes.opendatasoft.com/api/records/1.0/search/"

def main():
    # Ask user for optional municipality filter
    municipality = input("Enter the municipality name (leave blank for all): ").strip()

    params = {
        "dataset": "25-plr-producao-renovavel",
        "rows": 1000
    }

    if municipality:
        params["refine.concelho"] = municipality

    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        records = response.json().get("records", [])
        if not records:
            print("No data found for the provided filters.")
            return

        # Extract relevant fields
        data = []
        for item in records:
            fields = item.get("fields", {})
            data.append({
                "Municipality": fields.get("concelho", ""),
                "Year": fields.get("ano", ""),
                "Installed Capacity (kW)": fields.get("potencia_de_ligacao", 0)
            })

        df = pd.DataFrame(data)

        if df.empty:
            print("No numeric data available to display.")
            return

        # Show results in terminal
        print("\nResults:")
        print(df)

        # Ask if user wants to export to Excel
        save = input("Save results to Excel file? (y/n): ").strip().lower()
        if save == "y":
            output_file = "renewable_capacity_results.xlsx"
            df.to_excel(output_file, index=False)
            print(f"File saved: {output_file}")
        else:
            print("Results were not saved.")
    else:
        print("Error accessing the API. Please check the URL or try again later.")

if __name__ == "__main__":
    main()
