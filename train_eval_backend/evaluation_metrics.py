from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_squared_error, mean_absolute_error, r2_score
)
from sklearn.exceptions import UndefinedMetricWarning
import warnings

class MetricsEvaluator:
    """
    Class to handle the calculation of various evaluation metrics.
    """

    def __init__(self):
        """
        Initializes the EvaluationMetrics class.
        """
        # Dictionary mapping metric names to their corresponding functions
        self.evaluation_functions = {
            # Classification
            'accuracy': accuracy_score,
            'precision': lambda y_true, y_pred: precision_score(y_true, y_pred, average='weighted'),
            'recall': lambda y_true, y_pred: recall_score(y_true, y_pred, average='weighted'),
            'f1_score': lambda y_true, y_pred: f1_score(y_true, y_pred, average='weighted'),
            # Regression
            'mae': mean_absolute_error,
            'mse': mean_squared_error,
            'r2_score': r2_score,
        }

    def calculate_metric(self, metric_name, y_true, y_pred):
        """
        Calculate the specified metric.

        Args:
            metric_name (str): Name of the metric to calculate.
            y_true (array): True labels or values.
            y_pred (array): Predicted labels or values.

        Returns:
            float: The calculated metric, or None if an error occurs or the metric is undefined.
        """
        try:
            if metric_name in self.evaluation_functions:
                return self.evaluation_functions[metric_name](y_true, y_pred)
            else:
                print(f"Metric '{metric_name}' not recognized.")
                return None
        except UndefinedMetricWarning as e:
            print(f"Warning for metric '{metric_name}': {e}")
            return None
        except Exception as e:
            print(f"Error calculating metric '{metric_name}': {e}")
            return None
