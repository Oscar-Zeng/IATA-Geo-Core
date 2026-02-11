import pandas as pd
import math
import os

class AirportCalculator:
    """
    A core utility class for calculating Great Circle distances 
    between airports using curated IATA data.
    """

    def __init__(self, csv_path):
        """
        Initialize the calculator by loading the refined dataset.
        :param csv_path: Path to the iata_geo_core.csv file.
        """
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Database not found at: {csv_path}")
            
        self.df = pd.read_csv(csv_path)
        # Set IATA code as index for O(1) lookup performance
        self.df.set_index('iata', inplace=True)

    def get_airport_info(self, iata):
        """
        Retrieve latitude and longitude for a given IATA code.
        :param iata: 3-letter IATA airport code (e.g., 'PEK').
        :return: Pandas Series containing airport data or None if not found.
        """
        try:
            # Normalize to uppercase
            iata = iata.upper().strip()
            return self.df.loc[iata]
        except KeyError:
            return None

    def haversine(self, lat1, lon1, lat2, lon2):
        """
        Calculate the great-circle distance between two points on a sphere.
        Formula: d = 2r arcsin(sqrt(sin²(Δφ/2) + cos φ1 cos φ2 sin²(Δλ/2)))
        :return: Distance in miles (rounded to 2 decimal places).
        """
        # Convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = (math.sin(dlat / 2)**2 + 
             math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2)
        c = 2 * math.asin(math.sqrt(a))
        
        # Earth's radius in miles (use 6371 for kilometers)
        miles_radius = 3958.8
        distance = miles_radius * c
        return round(distance, 2)

    def calculate_distance(self, iata1, iata2):
        """
        High-level wrapper to calculate distance between two IATA codes.
        :param iata1: Origin airport IATA.
        :param iata2: Destination airport IATA.
        :return: Float (miles) or None if codes are invalid.
        """
        origin = self.get_airport_info(iata1)
        destination = self.get_airport_info(iata2)

        if origin is None or destination is None:
            return None

        return self.haversine(
            origin['lat'], origin['lon'], 
            destination['lat'], destination['lon']
        )

# --- Unit Test / Example Usage ---
if __name__ == "__main__":
  
    import os
    print(f"Current Directory: {os.getcwd()}")
    
    data_path = 'data/iata_geo_core.csv'
    
  
    if not os.path.exists(data_path):
        print(f"❌ Error: Cannot find file at {data_path}")
    else:
        try:
            calc = AirportCalculator(data_path)
            print("✅ Database loaded successfully!")
            
           
            test_iata = 'PEK'
            if calc.get_airport_info(test_iata) is not None:
                print(f"📍 Found {test_iata} in database.")
            else:
                print(f"❓ {test_iata} not found in CSV. Maybe check your refinement logic?")

           
            dist = calc.calculate_distance('PEK', 'JFK')
            if dist:
                print(f"✈️ Distance from PEK to JFK: {dist} miles")
            else:
                print("❌ Distance calculation failed (check IATA codes).")
                
        except Exception as e:
            print(f"💥 An error occurred: {e}")