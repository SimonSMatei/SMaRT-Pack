'''

    Gradient Boosting Regressor Wrappers for SMaRT_Pack.

    This module provides a scikit-learn compatible wrapper for Gradient Boosting
    Regression models, specifically optimized for materials informatics tasks
    within the SMaRT_Pack ecosystem.

'''

import pandas as pd
import numpy as np

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.base import BaseEstimator, RegressorMixin

class GBR(BaseEstimator, RegressorMixin):
    
    '''

        The GBR class is a scikit-learn compatible wrapper for Gradient Boosting
        Regression models, optimized for materials informatics tasks within the
        SMaRT_Pack ecosystem.

        Attributes:
            model_ (GradientBoostingRegressor): The underlying scikit-learn estimator.
            feature_importances_ (np.ndarray): Impurity-based feature importances.
            feature_names_in_ (np.ndarray): Names of features seen during fit.

    '''
    
    
    def __init__(
        self, 
        n_estimators: int = 500, 
        learning_rate: float = 0.01, 
        max_depth: int|None = None, 
        min_samples_split: int|None = None, 
        min_samples_leaf: int|None = None, 
        tol: float = 0.001, 
        warm_start: bool = True, 
        random_state: int|None = None, 
        loss: str = 'squared_error'
    ) -> None:

        '''

            This method initializes the GBR model with the specified hyperparameters.

            Args:
                n_estimators (int): The number of boosting stages to perform.
                learning_rate (float): The learning rate shrinks the contribution of each tree.
                max_depth (int|None): The maximum depth of the individual regression estimators.
                min_samples_split (int|None): The minimum number of samples required to split an internal node.
                min_samples_leaf (int|None): The minimum number of samples required to be at a leaf node.
                tol (float): Tolerance for stopping criterion.
                warm_start (bool): Whether to reuse the solution of the previous call to fit and continue fitting.
                random_state (int|None): The seed used by the random number generator.
                loss (str): The loss function to be optimized.

        '''
        
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

        '''

            This method fits the GBR model to the training data.

            Args:
                X (pd.DataFrame | np.ndarray): The training data.
                y (pd.Series | np.ndarray): The training labels.

            Returns:
                GBR: The fitted GBR model.

        '''
        
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

        '''

            This method predicts the labels for the input data.

            Args:
                X (pd.DataFrame | np.ndarray): The input data.

            Returns:
                np.ndarray: The predicted labels.

        '''
        
        return self.model_.predict(X)
    

    
    @property
    def feature_importances_(self) -> np.ndarray:

        '''

            This method returns the feature importances of the fitted GBR model.

            Returns:
                np.ndarray: The feature importances of the fitted GBR model.

        '''

        if not hasattr(self, 'model_'):

            raise ValueError("The model has not been fitted yet. Call .fit() first.")
        
        return self.model_.feature_importances_
    
    
    @property
    def feature_names_in_(self) -> np.ndarray:

        '''

            This method returns the feature names of the fitted GBR model.

            Returns:
                np.ndarray: The feature names of the fitted GBR model.

        '''

        if not hasattr(self, 'model_'):

            raise ValueError("The model has not been fitted yet. Call .fit() first.")
        
        if not hasattr(self.model_, 'feature_names_in_'):

            raise AttributeError("The model was not fitted with a Pandas DataFrame, so feature names are not available.")
        
        return self.model_.get_feature_names_in_
