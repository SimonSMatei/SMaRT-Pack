import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.base import BaseEstimator, RegressorMixin


def load_data(file_path:str) -> pd.DataFrame:
    script_dir = Path(file_path).resolve()

    if not script_dir.exists():
        raise FileNotFoundError(f"Critical error: Dataset missing at {script_dir}")

    return pd.read_csv(script_dir)

def find_outliers(y_hat: np.ndarray, y: np.ndarray, threshold: float = 3.0) -> np.ndarray:
    
    residuals = y - y_hat
    std_res = np.std(residuals)
    
    return np.where(np.abs(residuals) > threshold * std_res)[0]


class GBR(BaseEstimator, RegressorMixin):
    
    def __init__(self, learning_rate: float, max_depth: int, n_estimators: int, 
                min_samples_leaf: int, warm_start: bool, features: list[str], 
                loss:str = "squared_error") -> None:
        
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.n_estimators = n_estimators
        self.min_samples_leaf = min_samples_leaf 
        self.warm_start = warm_start
        self.loss = loss
        
        self.features = features  
    
    def fit(self, X: pd.DataFrame, y: pd.Series) -> 'GBR':

        parms = {  'learning_rate': self.learning_rate,
                    'max_depth': self.max_depth,
                    'n_estimators': self.n_estimators, 
                    'min_samples_leaf': self.min_samples_leaf, 
                    'warm_start': self.warm_start,
                    'loss': self.loss}
        
        self.model = GradientBoostingRegressor(**parms)

        X_filtered = X[self.features]

        self.model.fit(X_filtered, y)

        return self

    def predict(self, X: pd.DataFrame) -> np.ndarray:

        X_filtered = X[self.features]

        return self.model.predict(X_filtered)