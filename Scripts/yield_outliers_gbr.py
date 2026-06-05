from SMaRT_Pack.DevModelPrac import GradBoostReg as gbr
from pathlib import Path
from sklearn.model_selection import train_test_split

if __name__ == "__main__":
    features = ["temp_ratio", "delta_Eb0", "sigma_y0", "E_negativity", "volume_DISTORT", "Exp_Shear_DISTORT", "Exp_Youngs_ROM"]

    learning_rate = 0.01
    max_depth = 3
    n_estimators = 100
    min_samples_leaf = 6
    warm_start = True


    file_path = Path(__file__).resolve().parent.parent / "DataBases" / "MPEA_dataset_EXT.csv"

    data = gbr.load_data(file_path)

    gbr_model = gbr.GBR(learning_rate = learning_rate, max_depth = max_depth,
                          n_estimators = n_estimators, min_samples_leaf = min_samples_leaf,
                          warm_start = warm_start, features = features)

    X_train, X_test, y_train, y_test = train_test_split(data, data["Yield_EXP"], test_size = 0.2, random_state = 13)

    gbr_model.fit(X_train, y_train)

    r2_score_test = gbr_model.score(X_test, y_test)
    print(f'R2 Score (test): {r2_score_test:.4f}')
    
    r2_score_train = gbr_model.score(X_train, y_train)
    print(f'R2 Score (train): {r2_score_train:.4f}')

