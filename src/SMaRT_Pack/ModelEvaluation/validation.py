'''

    Model Validation and Evaluation for SMaRT_Pack.

    This module provides scikit-learn compatible model evaluation and validation
    tools, specifically optimized for materials informatics tasks within the
    SMaRT_Pack ecosystem.

'''


import pandas as pd
import numpy as np

from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.model_selection import RepeatedKFold, RepeatedStratifiedKFold


def kfold_cross_validation(
    model, X: pd.DataFrame | np.ndarray, 
    y: pd.Series | np.ndarray, 
    n_splits: int, 
    n_repeats: int, 
    stratified: bool = False, 
    random_state: int | None = None
    ) -> tuple[float, float, pd.DataFrame]:

    '''

        This method performs k-fold cross-validation on the input data.

        Args:
            model: The model to evaluate.
            X (pd.DataFrame | np.ndarray): The input data.
            y (pd.Series | np.ndarray): The target data.
            n_splits (int): The number of splits to perform.
            n_repeats (int): The number of repeats to perform.
            stratified (bool): Whether to perform stratified cross-validation.
            random_state (int | None): The seed used by the random number generator.

        Returns:
            tuple[float, float, pd.DataFrame]: The mean R², the standard deviation of R², and a DataFrame containing the metrics for each fold.

    '''
    
    scores = []


    if stratified:

        kfold = RepeatedStratifiedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state=random_state)

    else:
        
        kfold = RepeatedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state=random_state)


    X_arr = np.asarray(X)
    y_arr = np.asarray(y)

    fold_metrics = []
    
    for fold_idx, (train_idx, test_idx) in enumerate(kfold.split(X_arr, y_arr)):
    
        X_train, X_test = X_arr[train_idx], X_arr[test_idx]
    
        y_train, y_test = y_arr[train_idx], y_arr[test_idx]
        
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        
        score = r2_score(y_test, y_pred)
        
        scores.append(score)

        fold_metrics.append({

            'Fold': fold_idx,

            'R2': score,

        })
    
    results = pd.DataFrame(fold_metrics)

    results.set_index('Fold', inplace=True)
    
    return np.mean(scores), np.std(scores), results


def get_performance_metrics(y_true: pd.Series | np.ndarray, y_pred: pd.Series | np.ndarray) -> dict[str, float]:

    '''

        This method calculates the performance metrics for the input data.

        Args:
            y_true (pd.Series | np.ndarray): The true labels.
            y_pred (pd.Series | np.ndarray): The predicted labels.

        Returns:
            dict[str, float]: A dictionary containing the performance metrics.

    '''
    
    r2 = r2_score(y_true, y_pred)
    
    mae = mean_absolute_error(y_true, y_pred)
    
    mse = mean_squared_error(y_true, y_pred)
    
    rmse = np.sqrt(mse)

    relative_mae = mae / np.mean(y_true) * 100

    relative_rmse = rmse / np.mean(y_true) * 100

    return {

        'R2': r2,
        
        'MAE': mae,

        'MSE': mse,
        
        'RMSE': rmse,
        
        'Relative MAE': relative_mae,
        
        'Relative RMSE': relative_rmse,

    }


def get_outlier_report(y_hat: np.ndarray, y: np.ndarray, compositions: list[str] | pd.Series | np.ndarray, threshold: float = 3.0) -> pd.DataFrame:
    
    '''

        This method generates a report of outliers in the input data.

        Args:
            y_hat (np.ndarray): The predicted labels.
            y (np.ndarray): The true labels.
            compositions (list[str] | pd.Series | np.ndarray): The compositions of the input data.
            threshold (float): The threshold for identifying outliers.

        Returns:
            pd.DataFrame: A DataFrame containing the outlier report.

    '''
    
    outlier_ind, standard_errors = find_outliers(y_hat, y, threshold)
    
    compositions = np.asarray(compositions)

    bad_compositions = compositions[outlier_ind]

    bad_y = y[outlier_ind]
    
    bad_y_hat = y_hat[outlier_ind]

    bad_standard_errors = standard_errors[outlier_ind]

    report = pd.DataFrame({

        'Composition': bad_compositions,
        
        'y': bad_y,
        
        'y_hat': bad_y_hat,
        
        'Standardized Error': bad_standard_errors,

    })

    return report


def find_outliers(y_hat: np.ndarray, y: np.ndarray, threshold: float = 3.0) -> tuple[np.ndarray, np.ndarray]:

    '''

        This method finds outliers in the input data.

        Args:
            y_hat (np.ndarray): The predicted labels.
            y (np.ndarray): The true labels.
            threshold (float): The threshold for identifying outliers.

        Returns:
            tuple[np.ndarray, np.ndarray]: A tuple containing the indices of the outliers and the standardized errors.

    '''
    
    residuals = y - y_hat

    std_res = np.std(residuals)

    return np.where(np.abs(residuals) > threshold * std_res)[0], residuals / std_res
