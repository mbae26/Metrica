from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_squared_error, mean_absolute_error, r2_score
)

class MetricsEvaluator:
    """
    Class for handling the calculation of various evaluation metrics for machine learning models.
    """

    def __init__(self):
        """
        Initializes the MetricsEvaluator class with predefined evaluation functions.
        """
        self.evaluation_functions = {
            'classification': {
                'accuracy': accuracy_score,
                'precision': lambda y_true, y_pred: precision_score(y_true, y_pred, average='weighted'),
                'recall': lambda y_true, y_pred: recall_score(y_true, y_pred, average='weighted'),
                'f1_score': lambda y_true, y_pred: f1_score(y_true, y_pred, average='weighted'),
            },
            'regression': {
                'mae': mean_absolute_error,
                'mse': mean_squared_error,
                'r2_score': r2_score,
            }            
        }

    def calculate_metrics(self, task_type, y_true, y_pred):
        """
        Calculates a set of metrics based on the task type.

        Args:
            task_type (str): The type of the task ('classification' or 'regression').
            y_true (array-like): True labels or values.
            y_pred (array-like): Predicted labels or values.

        Returns:
            dict: A dictionary of calculated metrics.
        """
        scores = {}
        for metric_name, func in self.evaluation_functions[task_type].items():
            scores[metric_name] = func(y_true, y_pred)

        return scores