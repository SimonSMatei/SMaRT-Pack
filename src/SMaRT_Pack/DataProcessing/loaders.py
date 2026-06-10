'''
    
    Data loading utilities for the SMaRT_Pack pipeline.

    This module provides an interface to fetch materials science data from 
    online repositories, including the AFLOW database.

'''

import requests
import pandas as pd
from pathlib import Path


def load_aflow_data(url: str, save_csv: bool = False, csv_path: str | Path = None) -> pd.DataFrame | None:

    '''
       
        Loads data from the online AFLOW database into a Pandas DataFrame.

        This function fetches raw material data from a specified AFLOW URL. It 
        optionally serializes the resulting DataFrame to a CSV file if a path 
        is provided.

        Args:
            url (str): URL to the AFLOW database
            save_csv (bool): Whether to save the data to a CSV file
            csv_path (str | Path): Path to save the CSV file

        Returns:
            pd.DataFrame | None: DataFrame containing the AFLOW data

    '''

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

