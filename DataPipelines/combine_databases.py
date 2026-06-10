'''

    This script is used to combine the data from the ICSD and AFLOW databases into a single 
    pandas DataFrame.

    The data is loaded from the DataBases/RawData/ICSDCarbides and DataBases/RawData/AllAFLOWCarbides
    folders.

    The data is then saved as CSV files in the DataBases/RawData/CombinedData folder.

'''

### Imports ###

import pandas as pd
from pathlib import Path
from functools import reduce

### Directory Paths ###

RAW_DIR = Path(__file__).resolve().parent.parent / 'DataBases' / 'RawData'

ICSD_DIR = RAW_DIR / 'ICSDCarbides'

AFLOW_DIR = RAW_DIR / 'AllAFLOWCarbides'

### Functions ###

def load_and_merge_data(directory: Path) -> pd.DataFrame:

    '''

        This function loads all the data from the given directory and merges it into a single 
        pandas DataFrame.

        Args:
            directory (Path): The path to the directory containing the data.

        Returns:
            pd.DataFrame: The combined data.

    '''

    all_data = []

    for i in directory.glob('*.csv'):

        all_data.append(pd.read_csv(i))

    
    combined_data = reduce(lambda left, right: pd.merge(left, right, on = ['compound', 'auid', 'aurl', 'spacegroup_relax', 'Pearson_symbol_relax', 'species'], how = 'outer'), all_data)

    return combined_data


def remove_icsd_from_aflow(combined_icsd: pd.DataFrame, combined_aflow: pd.DataFrame) -> pd.DataFrame:

    '''

        This function removes the data from the ICSD database from the AFLOW database.

        Args:
            combined_icsd (pd.DataFrame): The combined data from the ICSD database.
            combined_aflow (pd.DataFrame): The combined data from the AFLOW database.

        Returns:
            pd.DataFrame: The combined data from the AFLOW database with the data from the ICSD database removed.

    '''

    icsd_ids = combined_icsd['auid'].unique()

    in_icsd = combined_aflow['auid'].isin(icsd_ids)

    combined_aflow = combined_aflow[~in_icsd]
    
    return combined_aflow


def save_to_csv(df: pd.DataFrame, directory: Path, file_name: str) -> None:

    """

        This function saves a pandas DataFrame to a CSV file.

        Args:
            df (pd.DataFrame): The DataFrame to save.
            directory (Path): The path to the directory to save the file in.
            file_name (str): The name of the file to save.

    """

    df.to_csv(directory / file_name, index = False)

### Main ###

if __name__ == '__main__':

    ### Load Data ###

    combined_icsd = load_and_merge_data(ICSD_DIR)

    combined_all = load_and_merge_data(AFLOW_DIR)

    combined_aflow = remove_icsd_from_aflow(combined_icsd, combined_all)

    ### Save Data ###

    save_to_csv(combined_icsd, RAW_DIR / 'CombinedData', 'combined_icsd.csv')

    save_to_csv(combined_aflow, RAW_DIR / 'CombinedData', 'combined_aflow.csv')

    save_to_csv(combined_all, RAW_DIR / 'CombinedData', 'combined_all.csv')
