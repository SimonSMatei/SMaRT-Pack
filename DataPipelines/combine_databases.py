import pandas as pd
from pathlib import Path
from functools import reduce

RAW_DIR = Path(__file__).resolve().parent.parent / 'DataBases' / 'RawData'
ICSD_DIR = RAW_DIR / 'ICSDCarbides'
AFLOW_DIR = RAW_DIR / 'AllAFLOWCarbides'

def load_and_merge_data(directory: Path) -> pd.DataFrame:
    all_data = []

    for i in directory.glob('*.csv'):
        all_data.append(pd.read_csv(i))
    
    combined_data = reduce(lambda left, right: pd.merge(left, right, on = ['compound', 'auid', 'aurl', 'spacegroup_relax', 'Pearson_symbol_relax', 'species'], how = 'outer'), all_data)

    return combined_data

def remove_icsd_from_aflow(combined_icsd: pd.DataFrame, combined_aflow: pd.DataFrame) -> pd.DataFrame:
    icsd_ids = combined_icsd['auid'].unique()
    in_icsd = combined_aflow['auid'].isin(icsd_ids)
    combined_aflow = combined_aflow[~in_icsd]
    
    return combined_aflow

def save_to_csv(df: pd.DataFrame, directory: Path, file_name: str) -> None:
    df.to_csv(directory / file_name, index = False)


if __name__ == '__main__':
    combined_icsd = load_and_merge_data(ICSD_DIR)
    combined_all = load_and_merge_data(AFLOW_DIR)

    combined_aflow = remove_icsd_from_aflow(combined_icsd, combined_all)

    save_to_csv(combined_icsd, RAW_DIR / 'CombinedData', 'combined_icsd.csv')
    save_to_csv(combined_aflow, RAW_DIR / 'CombinedData', 'combined_aflow.csv')
    save_to_csv(combined_all, RAW_DIR / 'CombinedData', 'combined_all.csv')