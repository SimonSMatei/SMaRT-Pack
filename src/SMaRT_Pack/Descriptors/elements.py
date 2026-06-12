import json
import pandas as pd
from pathlib import Path
from pymatgen.core.periodic_table import Element

class ElementData:

    def __init__ (self, elements: list[str], properties: list[str], custom_properties: dict[str, dict] | None = None) -> None:

        if not elements:
            raise ValueError("No elements provided")
        
        if not properties:
            raise ValueError("No properties provided")
        
        if custom_properties is None:
            self.custom_properties = {}
        elif not isinstance(custom_properties, dict):
            raise TypeError("custom_properties must be a dictionary or None")
        else:
            for prop, value in custom_properties.items():
                if not isinstance(prop, str):
                    raise TypeError(f"Property {prop} must be a string")
                if not isinstance(value, dict):
                    raise TypeError(f"{prop} must be a dictionary")
                for elem in value.keys():
                    if elem not in elements:
                        raise ValueError(f"Element {elem} not in elements list")
            
            self.custom_properties = custom_properties
        

        self._translator = {
            "electronegativity": "X",
            "atomic_number": "Z"
        }
  
        
        self.elements_map = {element: Element(element) for element in elements}

        sample_element = self.elements_map[elements[0]]

        valid_properties = []

        for prop in properties:

            py_prop = self._translator.get(prop, prop)

            if prop in self.custom_properties:
                valid_properties.append(prop)
            elif hasattr(sample_element, py_prop) or py_prop in sample_element.data:
                valid_properties.append(prop)
            else:
                raise ValueError(f"Property {prop} is not a valid property")
        
        for prop in self.custom_properties.keys():
            if prop not in valid_properties:
                valid_properties.append(prop)

        self.properties = valid_properties

        self.elements_matrix = self._get_elements_matrix()

    
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

        
    def _get_elements_matrix(self) -> dict[str, dict]:
        elements_matrix = {}
        for element, elem_obj in self.elements_map.items():            
            elements_matrix[element] = {prop: self._extract_value(elem_obj, prop) for prop in self.properties}

        return elements_matrix

    def _extract_value(self, elem_obj: Element, prop: str) -> float | int | None:

        py_prop = self._translator.get(prop, prop)

        if prop in self.custom_properties:
            if elem_obj.symbol in self.custom_properties[prop]:
                return self.custom_properties[prop][elem_obj.symbol]
            elif not (hasattr(elem_obj, py_prop) or py_prop in elem_obj.data):
                return None

        if py_prop in elem_obj.data:
            item = elem_obj.data.get(py_prop)
        else:
            item = getattr(elem_obj, py_prop, None)
        
        if (item == "no data" or item is None) and py_prop == 'metallic_radius':
            item = elem_obj.atomic_radius
        
        if item == 'no data':
            return None
        
        if type(item) is str:
            return self._clean_prop(item)

        return item

    def _clean_prop(self, item: str) -> float:
       
        item = item.split(' ')[0]

        return float(item)
        