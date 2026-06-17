"""

    Extracts physical property data for target elements from the Pymatgen database 
    and exports it as a structured CSV file within the DataBases/ProcessedData/Misc directory.

    Formats the resulting dataset to ensure structural compatibility with the processed 
    aflow.csv file. Additionally, this script serves as the primary reference implementation 
    for configuring and instantiating the ElementData extraction class.

"""

### Imports ###

from pathlib import Path
from SMaRT_Pack import ElementData

### Directory Paths ###

OUTPUT_DIR = Path(__file__).resolve().parent.parent / 'DataBases' / 'ProcessedData' / 'Misc'

### Elements and Properties ###

ELEMENTS_LIST = [

    'Al', 'Ce', 'Co', 'Cr', 'Cu', 'Fe', 'Hf', 'Ir', 'Mn', 
    'Mo', 'Nb', 'Ni', 'Os', 'Pa', 'Pd', 'Pu', 'Re', 'Rh',
    'Ru', 'Sc', 'Ta', 'Tc', 'Th', 'Ti', 'V', 'W', 'Y',
    'Zn', 'Zr', 'C'

]

ELEMENT_PROPERTIES = [

    "atomic_mass",
    "electronegativity",
    "atomic_radius",
    "metallic_radius",
    "Melting point",
    "Coefficient of linear thermal expansion",
    "Thermal conductivity",
    "Vickers hardness",
    "Bulk modulus",
    "Youngs modulus",
    "Poissons ratio",

]

VECS = {

    'vec': {

        'Al': 3, 'Ce': 4, 'Co': 9, 'Cr': 6, 'Cu': 2, 'Fe': 3, 'Hf': 4, 'Ir': 6, 'Mn': 4, 
        'Mo': 6, 'Nb': 5, 'Ni': 2, 'Os': 6, 'Pa': 5, 'Pd': 4, 'Pu': 6, 'Re': 7, 'Rh': 6,
        'Ru': 6, 'Sc': 3, 'Ta': 5, 'Tc': 6, 'Th': 4, 'Ti': 4, 'V': 5, 'W': 6, 'Y': 3,
        'Zn': 2, 'Zr': 4, 'C': 4

    }
    
}

### Main ###

if __name__ == '__main__':

    ### Get Element Data ###
    
    element_data = ElementData(ELEMENTS_LIST, ELEMENT_PROPERTIES, custom_properties=VECS)

    ### Renamed the Data Headers to Match Alfow Dataset ###

    element_data_df = element_data.to_dataframe()

    element_data_df.rename(

        columns = {
        
        'Melting Point': 'melting_point',

        'Coefficient of linear thermal expansion': 'thermal_expansion',

        'Thermal conductivity': 'thermal_conductivity',

        'Vickers hardness': 'vickers_hardness',
        
        'Bulk modulus': 'bulk_modulus',
        
        'Youngs modulus': 'youngs_modulus',
        
        'Poissons ratio': 'poissons_ratio',

        }, 

        inplace = True
        
    )

    element_data_df.to_csv(OUTPUT_DIR / 'element_data.csv', index=False)
