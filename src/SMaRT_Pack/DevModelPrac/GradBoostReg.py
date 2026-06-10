'''

    The GradientBoostingRegressor class in this folder is to be used as a 
    practiec in developing ML models. The class is to be trained on data
    processed through the DataProcessing module and is to be used to 
    predict the target feature of the processed data. 

    This class is not intended to be used in the final SMaRT_Pack pipeline. 
    It is simply a template for developing ML models.

'''

import pandas as pd
import numpy as np

from pathlib import Path

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.base import BaseEstimator, RegressorMixin


def load_data(file_path:str) -> pd.DataFrame:

    '''

        Loads data from a CSV file into a Pandas DataFrame.

        Args:
            file_path (str): Path to the CSV file

        Returns:
            pd.DataFrame: DataFrame containing the data

    '''

    script_dir = Path(file_path).resolve()

    if not script_dir.exists():

        raise FileNotFoundError(f"Critical error: Dataset missing at {script_dir}")


    return pd.read_csv(script_dir)



def find_outliers(y_hat: np.ndarray, y: np.ndarray, threshold: float = 3.0) -> np.ndarray:

    '''

        Finds outliers in the predicted values of a model.

        Args:
            y_hat (np.ndarray): Predicted values
            y (np.ndarray): True values
            threshold (float): Threshold for the mean relative error

        Returns:
            np.ndarray: Array of indices of the outliers

    '''
    
    residuals = y - y_hat

    std_res = np.std(residuals)
    
    return np.where(np.abs(residuals) > threshold * std_res)[0]



class GBR(BaseEstimator, RegressorMixin):
    
    '''
    
        A simple implementation of a GradientBoostingRegressor to be used 
        for learning the basics of machine learning.
    
    '''
    
    def __init__(self, learning_rate: float, max_depth: int, n_estimators: int, 
                min_samples_leaf: int, warm_start: bool, features: list[str], 
                loss:str = "squared_error") -> None:

        '''

            Initializes the GradientBoostingRegressor class.

            Args:
                learning_rate (float): Learning rate for the model
                max_depth (int): Maximum depth of the model
                n_estimators (int): Number of estimators in the model
                min_samples_leaf (int): Minimum number of samples required to be at a leaf node
                warm_start (bool): Whether to use warm start
                features (list[str]): List of features to use for the model
                loss (str): Loss function to use for the model

            Returns:
                None

        '''
        
        self.learning_rate = learning_rate

        self.max_depth = max_depth
        
        self.n_estimators = n_estimators
        
        self.min_samples_leaf = min_samples_leaf 
        
        self.warm_start = warm_start
        
        self.loss = loss
        
        self.features = features

    
    def fit(self, X: pd.DataFrame, y: pd.Series) -> 'GBR':

        '''

            Fits the GradientBoostingRegressor class to the training data.

            Args:
                X (pd.DataFrame): Training data
                y (pd.Series): Target values

            Returns:
                'GBR': Fitted GradientBoostingRegressor class

        '''
        
        parms = { 

            'learning_rate': self.learning_rate,

            'max_depth': self.max_depth,

            'n_estimators': self.n_estimators, 

            'min_samples_leaf': self.min_samples_leaf, 

            'warm_start': self.warm_start,

            'loss': self.loss

        }
        
        self.model = GradientBoostingRegressor(**parms)

        X_filtered = X[self.features]

        self.model.fit(X_filtered, y)

        return self


    def predict(self, X: pd.DataFrame) -> np.ndarray:

        '''

            Predicts the target values of the input data.

            Args:
                X (pd.DataFrame): Input data

            Returns:
                np.ndarray: Predicted values

        '''

        X_filtered = X[self.features]

        return self.model.predict(X_filtered)
