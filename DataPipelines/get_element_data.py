from pathlib import Path
from SMaRT_Pack import ElementData

OUTPUT_DIR = Path(__file__).resolve().parent.parent / 'DataBases' / 'ProcessedData' / 'Misc'

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
    'VEC': {
        'Al': 3, 'Ce': 4, 'Co': 9, 'Cr': 6, 'Cu': 2, 'Fe': 3, 'Hf': 4, 'Ir': 6, 'Mn': 4, 
        'Mo': 6, 'Nb': 5, 'Ni': 2, 'Os': 6, 'Pa': 5, 'Pd': 4, 'Pu': 6, 'Re': 7, 'Rh': 6,
        'Ru': 6, 'Sc': 3, 'Ta': 5, 'Tc': 6, 'Th': 4, 'Ti': 4, 'V': 5, 'W': 6, 'Y': 3,
        'Zn': 2, 'Zr': 4, 'C': 4
    }
}

element_data = ElementData(ELEMENTS_LIST, ELEMENT_PROPERTIES, custom_properties=VECS)

print(element_data.elements_matrix)

element_data.save_as_csv(OUTPUT_DIR / 'element_data.csv')
