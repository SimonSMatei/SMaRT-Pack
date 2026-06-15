import pandas as pd
import numpy as np

from sklearn.metrics import r2_score
from sklearn.model_selection import RepeatedKFold, RepeatedStratifiedKFold


def kfold_cross_validation(
    model, X: pd.DataFrame | np.ndarray, y: pd.Series | np.ndarray, 
    n_splits: int, n_repeats: int, stratified: bool = False, random_state: int | None = None
    ) -> tuple[float, float, pd.DataFrame]:
    
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


def get_outlier_report(y_hat: np.ndarray, y: np.ndarray, compositions: list[str] | pd.Series | np.ndarray, threshold: float = 3.0) -> pd.DataFrame:
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

    residuals = y - y_hat

    std_res = np.std(residuals)

    return np.where(np.abs(residuals) > threshold * std_res)[0], residuals / std_res