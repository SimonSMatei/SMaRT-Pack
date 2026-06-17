import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pathlib import Path


def plot_parity(y_true: pd.Series | np.ndarray, 
                y_pred: pd.Series | np.ndarray, 
                title: str, 
                y_label: str, 
                x_label: str | None = None,
                performance_metrics: dict[str, float] | None = None,
                outlier_report: pd.DataFrame | None = None, 
                save_path: Path | str | None = None,
                show: bool = False) -> None:

    # Adapted from rben24's HECPyrochlore repository.
    # Original source: https://github.com/rben24/HECPyrochlore/blob/master/src/build_models/train_model.py
    
    fig, ax = plt.subplots(figsize=(6, 6))

    ax.scatter(y_true, y_pred, alpha=0.75, edgecolors='k', linewidth=0.5, color='steelblue', zorder=3)

    low = min(y_true.min(), y_pred.min())
    high = max(y_true.max(), y_pred.max())
    pad = (high - low) * 0.05
    ax.plot([low - pad, high + pad], [low - pad, high + pad], 'r--', linewidth=1.2)

    if x_label:
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
    else:
        ax.set_xlabel(f'Actual {y_label}')
        ax.set_ylabel(f'Predicted {y_label}')
    
    if performance_metrics is None:
        ax.set_title(title)
    else:
        ax.set_title(
            f'{title}\n'
            f'R²={performance_metrics["R2"]:.3f}  '
            f'RMSE={performance_metrics["RMSE"]:.4f}  '
            f'MAE={performance_metrics["MAE"]:.4f}'
        )
    
    if outlier_report is not None and not outlier_report.empty:
        ax.scatter(outlier_report['y'], outlier_report['y_hat'], color='red', marker='x', s=80, linewidth=2, zorder=4)
    
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    
    if show:
        plt.show()
    else:
        plt.close(fig)

def plot_feature_importance():
    pass