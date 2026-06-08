import requests
import pandas as pd
from pathlib import Path

def load_aflow_data(url: str, save_csv: bool = False, csv_path: str | Path = None) -> pd.DataFrame | None:

    if save_csv and csv_path is None:
        raise ValueError("csv_path must be provided when save_csv is True")
    
    try:
        aflow_data = requests.get(url = url)

        aflow_data.raise_for_status()

        aflow_data = aflow_data.json()

        data = pd.DataFrame(aflow_data)

        if save_csv and csv_path is not None:
            csv_path = Path(csv_path)

            data.to_csv(csv_path, index = False)

        return data
        
    except Exception as e:
        print(f"Error: {e}")
        return None
