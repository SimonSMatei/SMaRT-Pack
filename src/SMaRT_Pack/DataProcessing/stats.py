import pandas as pd
import numpy as np

def evaluate_duplicate_variances(data: pd.DataFrame, target_feature: str | list[str], threshold: float = 0.05,
                                 excluded_params: list[str] | None = None, origin_col: str = 'source',
                                 custom_agg: dict[str, str] | None = None, source_a: str = 'a', 
                                 source_b: str = 'b') -> tuple[pd.DataFrame, pd.DataFrame]:
    
    if excluded_params is None:
        excluded_params = []

    if custom_agg is None:
        custom_agg = {}
    
    if isinstance(target_feature, str):
        target_feature = [target_feature]

    all_exclude_params = set(excluded_params + target_feature)
    
    header = [i for i in data.columns.to_list() if i not in all_exclude_params]

    data_dups = data[data.duplicated(subset=target_feature, keep=False)].copy()

    var_output = {}
    
    for col in header:
        col_var = data_dups.groupby(target_feature)[col].apply(_calc_variances)

        var_output[col] = col_var.mean()

    base_agg = {}

    for i in excluded_params:
        base_agg[i] = 'first'

    for key, value in var_output.items():
        if pd.isna(value):
            base_agg[key] = 'first'
        elif value < threshold:
            base_agg[key] = 'mean'
        else:
            base_agg[key + '_' + source_a] = 'first'
            base_agg[key + '_' + source_b] = 'first'
            data = _split_divergent_columns(data, key, source_a, source_b, origin_col)
    
    base_agg = base_agg | custom_agg

    data = data.groupby(target_feature, as_index = False).agg(base_agg)

    var = pd.DataFrame(list(var_output.items()), columns = ['parameter', 'mean_variance'])

    return data, var
    

def _split_divergent_columns(data: pd.DataFrame, col: str, 
                             source_a: str, source_b: str, origin_col: str) -> pd.DataFrame:
    
    target_ind = data.columns.get_loc(col)

    data.insert(
        loc = target_ind,
        column = f'{col}_{source_a}',
        value = np.where(
            data[origin_col] == source_a,
            data[col],
            np.nan
        )
    )

    data.insert(
        loc = target_ind + 2,
        column = f'{col}_{source_b}',
        value = np.where(
            data[origin_col] == source_b,
            data[col],
            np.nan
        )
    )

    data = data.drop(columns = [col])

    return data

def _calc_variances(data: pd.Series) -> float:
    
    a, b = data.values

    if pd.isna(a) or pd.isna(b):
        return float('nan')

    maximum = max(abs(a), abs(b))

    if maximum == 0:
        return 0.0
    
    return abs(a - b) / maximum
