import json
import pandas as pd
from pathlib import Path
from pymatgen.core.periodic_table import Element

class ElementData:

    def __init__ (self, elements: list[str], properties: list[str]) -> None:

        if not elements:
            raise ValueError("No elements provided")
        
        if not properties:
            raise ValueError("No properties provided")
        
        self.elements_map = {element: Element(element) for element in elements}

        sample_element = self.elements_map[elements[0]]

        valid_properties = []

        for prop in properties:
            if hasattr(sample_element, prop) or prop in sample_element.data:
                valid_properties.append(prop)
            else:
                raise ValueError(f"Property {prop} is not a valid property")
                
        self.properties = valid_properties
  
    def get_elements_matrix(self) -> dict[str, dict]:
        self.elements_matrix = {}

        for element, elem_obj in self.elements_map.items():            
            self.elements_matrix[element] = {prop: self._extract_value(elem_obj, prop) for prop in self.properties}

        return self.elements_matrix
    
    def to_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame.from_dict(self.elements_matrix, orient='index')
        df.index.name = 'Composition'
        df = df.reset_index()

        return df

    def save_as_csv(self, file_path: str | Path) -> None:
        self.to_dataframe().to_csv(file_path, index=False)
    
    def save_as_parquet(self, file_path: str | Path) -> None:
        self.to_dataframe().to_parquet(file_path, index=False)

    def save_as_json(self, file_path: str | Path) -> None:
        with open(file_path, 'w') as f:
            json.dump(self.elements_matrix, f, indent=4)


    def _extract_value(self, elem_obj: Element, prop: str) -> float | int | None:
        if prop in elem_obj.data:
            item = elem_obj.data.get(prop)
        else:
            item = getattr(elem_obj, prop, None)
        
        if (item == "no data" or item is None) and prop == 'metallic_radius':
            item = elem_obj.atomic_radius
        
        if item == 'no data':
            return None
        
        if type(item) is str:
            return self._clean_prop(item)

        return item

    def _clean_prop(self, item: str) -> float:
       
        item = item.split(' ')[0]

        return float(item)
        