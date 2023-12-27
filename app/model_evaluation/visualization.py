import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import roc_curve, auc, precision_recall_curve, confusion_matrix

class ModelVisualizer:
    """
    A class for visualizing machine learning model performance and results.

    Attributes:
        save_path (str): Path where the visualizations and results will be saved.
    """

    def __init__(self, save_path):
        """
        Initializes the ModelVisualizer with a path to save visualizations and results.

        Args:
            save_path (str): The directory path where visualizations and results will be saved.
        """
        self.save_path = save_path
        self.model_names_dict = {
            'user_model': 'User Model', # Maybe change to given name for plots?
            'LogisticRegression': 'Logistic Regression',
            'DecisionTree_Classification': 'Decision Tree',
            'RandomForest_Classification': 'Random Forest',
            'AdaBoost': 'AdaBoost',
            'ShallowNN_Classification': 'Shallow Neural Network',
            'LinearRegression': 'Linear Regression',
            'LassoRegression': 'Lasso Regression',
            'DecisionTree_Regression': 'Decision Tree',
            'RandomForest_Regression': 'Random Forest',
            'GradientBoosting_Regression': 'Gradient Boosting',
            'ShallowNN_Regression': 'Shallow Neural Network',
        }
        self.plot_functions = {
            'roc_curve': self._plot_roc_curve,
            'precision_recall_curve': self._plot_precision_recall_curve,
            'residuals': self._plot_residuals,
            'prediction_vs_actual': self._plot_prediction_vs_actual
        }
        self.plot_types = {
            'classification': ['roc_curve', 'precision_recall_curve'],
            'regression': ['residuals', 'prediction_vs_actual']
        }

    def _assign_colors_to_models(self, results):
        """Assigns a unique color to each model for consistent plotting."""
        colors = sns.color_palette("hsv", len(results))
        return {model_name: color for model_name, color in zip(results.keys(), colors)}
    
    def _plot_roc_curve(self, y_true, y_scores, ax, label=None, color='blue'):
        """Plots the ROC curve on the given axis."""
        fpr, tpr, _ = roc_curve(y_true, y_scores)
        roc_auc = auc(fpr, tpr)
        ax.plot(fpr, tpr, label=f'{label} (AUC = {roc_auc:.2f})' if label else f'ROC Curve (AUC = {roc_auc:.2f})', color=color)
        ax.plot([0, 1], [0, 1], linestyle='--', color='grey')
        ax.set_xlabel('False Positive Rate')
        ax.set_ylabel('True Positive Rate')
        ax.set_title('Receiver Operating Characteristic')
        ax.legend(loc="lower right")


    def _plot_precision_recall_curve(self, y_true, y_scores, ax, label=None, color='blue'):
        """Plots the precision-recall curve on the given axis."""
        precision, recall, _ = precision_recall_curve(y_true, y_scores)
        ax.step(recall, precision, where='post', label=label if label else 'Precision-Recall Curve', color=color)
        ax.set_xlabel('Recall')
        ax.set_ylabel('Precision')
        ax.set_title('Precision-Recall Curve')
        ax.set_ylim([0.0, 1.05])
        ax.set_xlim([0.0, 1.0])
        ax.legend()

    def _plot_confusion_matrix(self, y_true, y_pred, ax, class_names, title):
        """Plots the confusion matrix on the given axis."""
        cm = confusion_matrix(y_true, y_pred)

        # Handle case where class_names is None
        if class_names is None:
            unique_labels = np.unique(np.concatenate((y_true, y_pred)))
            class_names = [str(label) for label in unique_labels]

        sns.heatmap(cm, annot=True, fmt="d", cmap='Blues', 
                    xticklabels=class_names, yticklabels=class_names, ax=ax)
        ax.set_xlabel('Predicted labels')
        ax.set_ylabel('True labels')
        ax.set_title(title)

    def _plot_residuals(self, y_true, y_pred, ax, label=None):
        """Plots the residuals on the given axis."""
        residuals = y_true - y_pred
        ax.scatter(y_pred, residuals, label=label if label else 'Residuals')
        ax.hlines(y=0, xmin=y_pred.min(), xmax=y_pred.max(), colors='red', linestyles='--')
        ax.set_xlabel('Predicted Values')
        ax.set_ylabel('Residuals')
        ax.set_title('Residual Plot')
        if label:
            ax.legend()

    def _plot_prediction_vs_actual(self, y_true, y_pred, ax, label=None):
        """Plots the prediction vs actual values on the given axis."""
        ax.scatter(y_true, y_pred, alpha=0.3, label=label if label else 'Predicted vs Actual')
        ax.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], '--', color='red')
        ax.set_xlabel('Actual Values')
        ax.set_ylabel('Predicted Values')
        ax.set_title('Predicted vs. Actual Values')
        if label:
            ax.legend()

    def _generate_results_table(self, results):
        """
        Generates a table from the evaluation results and saves it as an image.

        Args:
            results (dict): A dictionary containing evaluation scores for each model.

        Returns:
            pd.DataFrame: A DataFrame representing the results in tabular format.
        """
        # Filter out unwanted keys and rename model names
        filtered_results = {}
        for model_name, model_data in results.items():
            readable_name = self.model_names_dict.get(model_name, model_name)
            filtered_results[readable_name] = {k: v for k, v in model_data.items() if k not in ['y_test', 'predictions', 'y_scores', 'task_type']}

        # Create DataFrame from filtered results
        results_df = pd.DataFrame.from_dict(filtered_results, orient='index')
        results_df.reset_index(inplace=True)
        results_df.rename(columns={'index': 'Model Name'}, inplace=True)

        # Format numbers for better display
        results_df = results_df.map(lambda x: f'{x:.4f}' if isinstance(x, (float, int)) else x)

        # Plotting and styling
        fig, ax = plt.subplots(figsize=(12, len(results_df) * 0.4))
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=results_df.values, colLabels=results_df.columns, loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1.2, 1.5)

        sns.set_style("whitegrid")
        plt.title('Model Evaluation Results', pad=20)

        plt.savefig(os.path.join(self.save_path, "results_table.png"), bbox_inches='tight', pad_inches=0.05)
        plt.close()

        return results_df

    def _create_confusion_matrices(self, results, class_names=None):
        """
        Creates and saves confusion matrix visualizations for each model in the results.

        Args:
            results (dict): Dictionary containing evaluation results for each model.
            class_names (list of str, optional): Class names for classification labels.
        """
        num_models = len(results)
        # Calculate grid size for subplots
        grid_size = int(np.ceil(np.sqrt(num_models)))
        fig, axes = plt.subplots(grid_size, grid_size, figsize=(grid_size * 6, grid_size * 6))
        fig.suptitle('Confusion Matrices for All Models', fontsize=16)

        # Flatten axes array for easy indexing
        axes = axes.flatten()

        for idx, (model_name, model_results) in enumerate(results.items()):
            model_name = self.model_names_dict[model_name]
            y_test = model_results['y_test']
            predictions = model_results['predictions']
            ax = axes[idx]

            # Call the plotting function for each model
            self._plot_confusion_matrix(y_test, predictions, ax, class_names, 
                                        title=f'Confusion Matrix for {model_name}')

        # Hide unused subplots
        for idx in range(num_models, len(axes)):
            fig.delaxes(axes[idx])

        plt.tight_layout()
        plt.subplots_adjust(top=0.9)  # Adjust the top padding
        plt.savefig(os.path.join(self.save_path, "all_confusion_matrices.png"))
        plt.close()
    
    def _create_standard_plots(self, plot_name, results, model_colors):
        fig, ax = plt.subplots(figsize=(8, 6))
        plot_function = self.plot_functions[plot_name]

        for model_name, model_results in results.items():
            color = model_colors[model_name]
            model_name = self.model_names_dict[model_name]
            y_test = model_results['y_test']
            y_scores = model_results.get('y_scores', None)

            if y_scores is not None:
                plot_function(y_test, y_scores, ax, label=model_name, color=color)

        ax.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(self.save_path, f"{plot_name}.png"))
        plt.close()

    def _create_individual_plots(self, plot_name, results):
        num_models = len(results)
        grid_size = int(np.ceil(np.sqrt(num_models)))
        fig, axes = plt.subplots(grid_size, grid_size, figsize=(grid_size * 6, grid_size * 6))
        fig.suptitle(f'{plot_name.replace("_", " ").title()} for All Models', fontsize=16)
        axes = axes.flatten()

        for idx, (model_name, model_results) in enumerate(results.items()):
            model_name = self.model_names_dict[model_name]
            ax = axes[idx]
            y_test = model_results['y_test']
            predictions = model_results['predictions']
            self.plot_functions[plot_name](y_test, predictions, ax)
            ax.set_title(f'{model_name}')

        for idx in range(num_models, len(axes)):
            fig.delaxes(axes[idx])

        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        plt.savefig(os.path.join(self.save_path, f"{plot_name}_all_models.png"))
        plt.close()

    def create_visualizations(self, results):
        """
        Creates and saves visualizations for all models in the results.

        Args:
            results (dict): Dictionary containing evaluation results for each model.
        """
        try:
            task_type = next(iter(results.values()))['task_type']
            model_colors = self._assign_colors_to_models(results)

            for plot_name in self.plot_types[task_type]:
                if plot_name in ['roc_curve', 'precision_recall_curve']:
                    self._create_standard_plots(plot_name, results, model_colors)
                elif plot_name in ['residuals', 'prediction_vs_actual']:
                    self._create_individual_plots(plot_name, results)

            self._generate_results_table(results)
            if task_type == 'classification':
                self._create_confusion_matrices(results)
        
        except Exception as e:
            print(f"Error in creating visualizations: {e}")