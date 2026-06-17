"""

    An extraction engine that retrieves, validates, and standardizes physical 
    property data for a specified list of chemical elements.

    This class serves as a resilient ETL (Extract, Transform, Load) pipeline. It pulls 
    baseline properties from the pymatgen database while allowing users to safely inject 
    custom empirical data (e.g., specific Valence Electron Concentrations) via an 
    interceptor dictionary. It automatically handles structural validation, executes 
    logical fallbacks for missing data, strips string-based units for machine-learning 
    readiness, and generates a structured Pandas DataFrame.


    Parameters:

        elements (list of str): A list of chemical symbols representing the target elements.

        properties (list of str): A list of the target physical properties to extract.

        custom_properties (dict, optional): A nested dictionary containing explicit 
            user-defined values that override or supplement the default database. 
            Expected format: {'property_name': {'Element_Symbol': value}}. Defaults to None.

"""

### Imports ###

import json
import pandas as pd
import warnings
from pathlib import Path
from pymatgen.core.periodic_table import Element

### Class ###

class ElementData:

    def __init__ (self, elements: list[str], properties: list[str], custom_properties: dict[str, dict] | None = None) -> None:

        """

            Initialize the ElementData class

            Args:

                elements (list[str]): A list of chemical symbols representing the target elements.

                properties (list[str]): A list of the target physical properties to extract.

                custom_properties (dict, optional): A nested dictionary containing explicit 
                    user-defined values that override or supplement the default database. 
                    Expected format: {'property_name': {'Element_Symbol': value}}. Defaults to None.

        """

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

        """

            This function converts the elements matrix to a pandas DataFrame.

            Returns:

                pd.DataFrame: The elements matrix as a pandas DataFrame.

        """

        df = pd.DataFrame.from_dict(self.elements_matrix, orient='index')

        df.index.name = 'composition'
        
        df = df.reset_index()

        return df


    def save_as_csv(self, file_path: str | Path) -> None:

        """

            This function saves the elements matrix to a CSV file.

            Args:

                file_path (str | Path): The path to the CSV file to save.

        """

        self.to_dataframe().to_csv(file_path, index=False)
    
    
    def save_as_parquet(self, file_path: str | Path) -> None:

        """

            This function saves the elements matrix to a parquet file.

            Args:

                file_path (str | Path): The path to the parquet file to save.

        """

        self.to_dataframe().to_parquet(file_path, index=False)


    def save_as_json(self, file_path: str | Path) -> None:

        """

            This function saves the elements matrix to a JSON file.

            Args:

                file_path (str | Path): The path to the JSON file to save.

        """

        with open(file_path, 'w') as f:
            
            json.dump(self.elements_matrix, f, indent=4)

        
    def _get_elements_matrix(self) -> dict[str, dict]:

        """

            This function creates a matrix of the elements and their properties.

            Returns:

                dict[str, dict]: The elements matrix.

        """

        elements_matrix = {}

        for element, elem_obj in self.elements_map.items():     

            elements_matrix[element] = {prop: self._extract_value(elem_obj, prop) for prop in self.properties}

        return elements_matrix


    def _extract_value(self, elem_obj: Element, prop: str) -> float | int | None:

        """

            This function extracts the value of a property from an element.

            Args:

                elem_obj (Element): The element to extract the property from.

                prop (str): The property to extract.

            Returns:

                float | int | None: The value of the property.

        """

        py_prop = self._translator.get(prop, prop)

        if prop in self.custom_properties:

            if elem_obj.symbol in self.custom_properties[prop]:
                
                return self.custom_properties[prop][elem_obj.symbol]
            
            elif not (hasattr(elem_obj, py_prop) or py_prop in elem_obj.data):
                
                return None

        if py_prop in elem_obj.data:
            
            item = elem_obj.data.get(py_prop)
        
        else:

            with warnings.catch_warnings():

                warnings.simplefilter("ignore")

                item = getattr(elem_obj, py_prop, None)
        
        if (item == "no data" or item is None) and py_prop == 'metallic_radius':
            
            item = elem_obj.atomic_radius
        
        if item == 'no data':
            
            return None
        
        if type(item) is str:

            return self._clean_prop(item)

        return item


    def _clean_prop(self, item: str) -> float:

        """

            This function cleans the value of a property.

            Args:

                item (str): The property to clean.

            Returns:

                float: The cleaned property value.

        """
        

        item = item.split(' ')[0]

        return float(item)
        