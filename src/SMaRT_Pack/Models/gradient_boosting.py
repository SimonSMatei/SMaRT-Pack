import pandas as pd
import numpy as np

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.base import BaseEstimator, RegressorMixin

class GBR(BaseEstimator, RegressorMixin):
    
    def __init__(self, n_estimators: int = 500, learning_rate: float = 0.01, max_depth: int|None = None, 
                min_samples_split: int|None = None, min_samples_leaf: int|None = None, tol: float = 0.001, 
                warm_start: bool = True, random_state: int|None = None, loss: str = 'squared_error') -> None:
        
        self.n_estimators = n_estimators
        
        self.learning_rate = learning_rate
        
        self.max_depth = max_depth
        
        self.min_samples_split = min_samples_split
        
        self.min_samples_leaf = min_samples_leaf
        
        self.tol = tol
        
        self.warm_start = warm_start
        
        self.random_state = random_state
        
        self.loss = loss
    
    def fit(self, X: pd.DataFrame | np.ndarray, y: pd.Series | np.ndarray) -> 'GBR':
        
        parms = {

            'n_estimators': self.n_estimators, 

            'learning_rate': self.learning_rate,

            'max_depth': self.max_depth,

            'min_samples_split': self.min_samples_split,

            'min_samples_leaf': self.min_samples_leaf, 

            'tol': self.tol,

            'warm_start': self.warm_start,

            'loss': self.loss,

            'random_state': self.random_state

        }

        self.model_ = GradientBoostingRegressor(**parms)

        self.model_.fit(X, y)

        return self

    def predict(self, X: pd.DataFrame | np.ndarray) -> np.ndarray:
        
        return self.model_.predict(X)
    

    @property
    def feature_importances_(self) -> np.ndarray:

        if not hasattr(self, 'model_'):

            raise ValueError("The model has not been fitted yet. Call .fit() first.")
        
        return self.model_.feature_importances_
    
    @property
    def feature_names_in_(self) -> np.ndarray:

        if not hasattr(self, 'model_'):

            raise ValueError("The model has not been fitted yet. Call .fit() first.")
        
        if not hasattr(self.model_, 'feature_names_in_'):

            raise AttributeError("The model was not fitted with a Pandas DataFrame, so feature names are not available.")
        
        return self.model_.get_feature_names_in_