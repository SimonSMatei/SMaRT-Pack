import ast
import pandas as pd
from pathlib import Path
from SMaRT_Pack import evaluate_duplicate_variances

DATA_DIR = Path(__file__).resolve().parent.parent / 'DataBases' / 'RawData' / 'CombinedData'
OUTPUT_DIR = Path(__file__).resolve().parent.parent / 'DataBases' / 'ProcessedData'

aflow_data = pd.read_csv(DATA_DIR / 'combined_aflow.csv')
icsd_data = pd.read_csv(DATA_DIR / 'combined_icsd.csv')

def calc_lattice_parameter(df: pd.DataFrame) -> pd.DataFrame:
    target_ind = df.columns.get_loc('volume_cell')
    df.insert(
        loc = target_ind + 1,
        column = 'calculated_lattice_parameter',
        value = (df['volume_cell'] / df['natoms'] * 8)**(1/3)
    )
    return df

def split_spin(df: pd.DataFrame) -> pd.DataFrame:
    species = df['species']
    spin = df['spinD']

    species = species.apply(ast.literal_eval)
    spin = spin.apply(ast.literal_eval)

    spin_carbon = []
    spin_metal = []

    for i, j in zip(species, spin):
        if i[0] == 'C':
            spin_carbon.append(j[0])
            spin_metal.append(j[-1])
        else:
            spin_carbon.append(j[-1])
            spin_metal.append(j[0])
    
    new_spin = pd.DataFrame({
        'spin_carbon': spin_carbon,
        'spin_metal': spin_metal
    }, index = df.index)
    
    return new_spin

def insert_new_spin(df: pd.DataFrame) -> pd.DataFrame:
    target_ind = df.columns.get_loc('spinD')

    new_spin = split_spin(df)

    df.insert(
        loc = target_ind,
        column = 'spinD_carbon',
        value = new_spin['spin_carbon']
    )

    df.insert(
        loc = target_ind + 1, 
        column = 'spinD_metal', 
        value = new_spin['spin_metal']
    )

    return df.drop(columns = ['spinD'])

def compress_data(df: pd.DataFrame) -> pd.DataFrame:
    drop_parameters = ['auid', 'aurl', 'spacegroup_relax', 'Pearson_symbol_relax', 'volume_cell', 'natoms']

    df = df.drop(columns = drop_parameters)

    df = create_compound_count(df)

    agg_dict = {
        'species': 'first',
        'spinD_carbon': 'mean',
        'spinD_metal': 'mean',
        'Egap': 'mean',
        'agl_thermal_expansion_300K': 'mean',
        'agl_debye': 'mean',
        'enthalpy_formation_atom': 'mean',
        'calculated_lattice_parameter': 'mean',
        'ael_bulk_modulus_vrh': 'mean',
        'ael_poisson_ratio': 'mean',
        'ael_shear_modulus_vrh': 'mean',
        'ael_youngs_modulus_vrh': 'mean',
        'agl_thermal_conductivity_300K': 'mean',
        'run_count': 'first',
    }

    df = df.groupby('compound', as_index = False).agg(agg_dict)

    return df
    
def create_compound_count(df: pd.DataFrame)->pd.DataFrame:
    df['run_count'] = df.groupby('compound')['compound'].transform('count')

    return df

def create_binding_col(df: pd.DataFrame)->pd.DataFrame:   
    target_ind = df.columns.get_loc('species')

    df.insert(
        loc = target_ind + 1,
        column = 'binding_metal',
        value = find_metal(df)
    )

    df = df.drop(columns = ['species'])

    return df

def find_metal(df: pd.DataFrame)->pd.Series:
    new_df = df['species'].apply(ast.literal_eval)
    new_df = new_df.apply(lambda x: [i for i in x if i != 'C'][0])

    return new_df

def combine_datasets(df1: pd.DataFrame, df2: pd.DataFrame)->pd.DataFrame:  
    df1['source'] = 'aflow'
    df2['source'] = 'icsd'

    return pd.concat([df1, df2], axis = 0)

def compress_combined_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    df, var = evaluate_duplicate_variances(
        data = df,
        target_feature = 'compound',
        excluded_params = ['binding_metal', 'run_count', 'source'], 
        origin_col = 'source',
        custom_agg = {'run_count': 'sum'},
        source_a = 'aflow',
        source_b = 'icsd'
    )

    return df, var


def sort_data(df: pd.DataFrame)->pd.DataFrame:  
    df = df.sort_values(by=['compound', 'source'])

    df = df.reset_index(drop=True)

    return df

def save_to_csv(df: pd.DataFrame, directory: Path, file_name: str) -> None:
    df.to_csv(directory / file_name, index = False)

if __name__ == '__main__':
    aflow_data = calc_lattice_parameter(aflow_data)
    icsd_data = calc_lattice_parameter(icsd_data)

    aflow_data = insert_new_spin(aflow_data)
    icsd_data = insert_new_spin(icsd_data)

    save_to_csv(aflow_data, OUTPUT_DIR, 'pre_compression_aflow.csv')
    save_to_csv(icsd_data, OUTPUT_DIR, 'pre_compression_icsd.csv')

    aflow_data = compress_data(aflow_data)
    icsd_data = compress_data(icsd_data)

    aflow_data = create_binding_col(aflow_data)
    icsd_data = create_binding_col(icsd_data)

    save_to_csv(aflow_data, OUTPUT_DIR, 'processed_aflow.csv')
    save_to_csv(icsd_data, OUTPUT_DIR, 'processed_icsd.csv')

    combined_data = combine_datasets(aflow_data, icsd_data)

    combined_data = sort_data(combined_data)

    save_to_csv(combined_data, OUTPUT_DIR, 'processed_all_uncompressed.csv')

    combined_data, var = compress_combined_dataset(combined_data)

    combined_data = sort_data(combined_data)

    combined_data = combined_data.drop(columns = ['source'])

    save_to_csv(var, OUTPUT_DIR, 'variances.csv')
    save_to_csv(combined_data, OUTPUT_DIR, 'processed_all.csv')
