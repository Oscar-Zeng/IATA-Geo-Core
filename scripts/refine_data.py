import os
import pandas as pd

# Remote source for global airport data provided by OurAirports
AIRPORTS_URL = "https://davidmegginson.github.io/ourairports-data/airports.csv"
# Local destination for the refined dataset
OUTPUT_PATH = os.path.join("data", "iata_geo_core.csv")

def refine_data() -> None:
    """
    Downloads raw airport data from OurAirports, filters it based on 
    commercial aviation criteria, and saves the refined core dataset.

    Filtering Rules:
    - Keep only rows with valid, non-empty IATA codes.
    - Filter by type: ['large_airport', 'medium_airport', 'small_airport'].
    - Keep only airports with 'scheduled_service' == 'yes'.
    - Column Selection: iata_code, name, municipality, iso_country, coordinates.
    - Standardize column names to: iata, name, city, country, lat, lon.
    """
    
    # Download and read the remote CSV data
    print(f"Fetching raw data from {AIRPORTS_URL}...")
    df = pd.read_csv(AIRPORTS_URL)

    # Define filtering criteria
    allowed_types = ["large_airport", "medium_airport", "small_airport"]
    
    # Apply filters: IATA existence, specific types, and active scheduled service
    df = df[
        df["iata_code"].notna()
        & (df["iata_code"].astype(str).str.strip() != "")
        & df["type"].isin(allowed_types)
        & (df["scheduled_service"] == "yes")
    ]

    # Select specific columns for the refined database
    cols = [
        "iata_code",
        "name",
        "municipality",
        "iso_country",
        "latitude_deg",
        "longitude_deg",
    ]
    df = df[cols]

    # Rename columns to standardized short names for better LLM/MCP processing
    df = df.rename(
        columns={
            "iata_code": "iata",
            "name": "name",
            "municipality": "city",
            "iso_country": "country",
            "latitude_deg": "lat",
            "longitude_deg": "lon",
        }
    )

    # Sort alphabetically by IATA code for better organization
    df = df.sort_values("iata")

    # Ensure the target directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # Save the refined commercial airport dataset to CSV
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Refinement complete. Curated data saved to {OUTPUT_PATH}")
    print(f"Total commercial airports indexed: {len(df)}")

if __name__ == "__main__":
    refine_data()