import requests
import pandas as pd

# API endpoint
API_URL = "https://e-redes.opendatasoft.com/api/explore/v2.1/catalog/datasets/capacidade-rececao-rnd/records"

def main():
    # Prompt for substation name
    installation = input("Enter installation name (leave blank for all): ").strip()

    # API parameters
    params = {
        "limit": 100  # Default limit
    }

    if installation:
        params["where"] = f"instalacao='{installation}'"

    # API request
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json().get("results", [])

        if not data:
            print("No data found for the specified filter.")
            return

        df = pd.DataFrame(data)

        # Ask if the user wants to save to Excel
        save = input("Save data to Excel file? (y/n): ").strip().lower()
        if save == "y":
            output_file = "substation_data.xlsx"  # Default filename
            df.to_excel(output_file, index=False)
            print(f"File saved as: {output_file}")
        else:
            print("Data was not saved.")
    else:
        print(f"API error: {response.status_code}\n{response.text}")

if __name__ == "__main__":
    main()
