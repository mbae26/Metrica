import os
import joblib
import json
import pandas as pd
from sklearn.metrics import accuracy_score, mean_squared_error

import model_registry
import evaluation_metrics as em


class RequestProcessor:
    """
    Handles the processing of a machine learning request which includes 
    training and evaluating models based on a given dataset.

    Attributes:
        request (Request): The request object containing details like task type and user information.
        s3_client (boto3.client): The S3 client for interacting with AWS S3.
        save_path (str): The directory path where trained models and results will be saved.
    """

    def __init__(self, request, s3_client):
        """
        Initializes the RequestProcessor with a request, S3 client, and save path.

        Args:
            request (Request): The request object.
            s3_client (boto3.client): The S3 client.
            save_path (str): The path where models and results are to be saved.
        """
        self.request = request
        self.s3_client = s3_client
        self.save_path = request.user_id
    
    def load_model(self):
        model_file_name = f"{self.save_path}_model"
        model_local_path = os.path.join('model', f"{self.save_path}.joblib")
        
        self.s3_client.download_file(model_file_name, model_local_path)
        
        model = joblib.load(model_local_path)
        return model

    def load_dataset(self, file_type):
        """
        Loads the dataset from S3.
        """
        dataset_file_name = f"{self.save_path}_{file_type}"
        dataset_local_path = os.path.join(file_type, f"{self.save_path}.csv")

        self.s3_client.download_file(dataset_file_name, dataset_local_path)

        dataset = pd.read_csv(dataset_local_path)

        X_train = dataset.iloc[:, :-1]
        y_train = dataset.iloc[:, -1]
        return X_train, y_train

    def train_model(self, model_name, model, X_train, y_train):
        """
        Trains the model.

        Args:
            model_name (str): The name of the model.
            model (sklearn.base.BaseEstimator): The machine learning model to train.
            X_train (pd.DataFrame): Training data features.
            y_train (pd.Series): Training data labels.
        """
        print(f'Training {model_name}...')
        model.fit(X_train, y_train)

    def evaluate_model(self, model, X_test, y_test, task_type):
        """
        Evaluates the model using specified metrics.

        Args:
            model (sklearn.base.BaseEstimator): The trained machine learning model.
            X_test (pd.DataFrame): Test data features.
            y_test (pd.Series): Test data labels.
            task_type (str): The type of task ('classification' or 'regression').

        Returns:
            dict: A dictionary containing evaluation scores and additional model outputs.
        """
        evaluator = em.MetricsEvaluator()
        evaluation_scores = {
            'y_test': y_test,
            'predictions': model.predict(X_test),
            'y_scores': model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None,
            'task_type': task_type
        }

        metrics_scores = evaluator.calculate_metrics(task_type, y_test, evaluation_scores['predictions'])
        evaluation_scores.update(metrics_scores)

        return evaluation_scores

    def save_model(self, model, model_name):
        """
        Saves the model to disk.

        Args:
            model (sklearn.base.BaseEstimator): The trained machine learning model.
            model_name (str): The name of the model.
        """
        model_save_path = os.path.join(self.save_path, f"{model_name}.joblib")
        joblib.dump(model, model_save_path, compress=True)
        print(f"Saved {model_name} model to {model_save_path}")

    def process_request(self):
        """
        Processes the request by training and evaluating models, and returns the results.

        Returns:
            dict: A dictionary of model names and their evaluation scores.
        """        
        X_train, y_train = self.load_dataset(file_type='train')
        X_test, y_test = self.load_dataset(file_type='test')

        task_type = self.request.task_type
        # # Load hyperparameters and model type from the specified JSON file
        # try:
        #     with open(self.request.hyperparams_path, 'r') as hp_file:
        #         model_config = json.load(hp_file)
        # except FileNotFoundError:
        #     print(f"Hyperparameters file not found: {self.request.hyperparams_path}")
        #     return
        # except json.JSONDecodeError:
        #     print(f"Error decoding JSON from file: {self.request.hyperparams_path}")
        #     return

        # hyperparams = model_config.get('hyperparameters', {})

        model_registry_dict = {}
        if task_type == 'classification':
            model_registry_dict = model_registry.classification_models
        elif task_type == 'regression':
            model_registry_dict = model_registry.regression_models

        results = {}
        for model_name, params in hyperparams.items():
            if model_name in model_registry_dict:
                model = model_registry_dict[model_name](**params)
                self.train_model(model_name, model, X_train, y_train)
                self.save_model(model, model_name)
                score = self.evaluate_model(model, X_test, y_test)
                results[model_name] = score
            else:
                print(f"Model '{model_name}' not found in {task_type} registry.")
                continue

        return results