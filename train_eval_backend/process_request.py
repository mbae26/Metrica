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

    def __init__(self, request, s3_client, save_path):
        """
        Initializes the RequestProcessor with a request, S3 client, and save path.

        Args:
            request (Request): The request object.
            s3_client (boto3.client): The S3 client.
            save_path (str): The path where models and results are to be saved.
        """
        self.request = request
        self.s3_client = s3_client
        self.save_path = save_path

    def load_dataset(self, path):
        """
        Loads the dataset from S3 and returns the training data and labels.

        Returns:
            Tuple[pd.DataFrame, pd.Series]: Training data features and labels.
        """
        dataset_file_name = f"train/{self.request.user_id}_{self.request.submission_time}.csv"
        dataset_local_path = os.path.join('datasets', dataset_file_name)

        try:
            self.s3_client.download_file(dataset_file_name, dataset_local_path)
        except Exception as e:
            print(f"Error downloading dataset from S3: {e}")
            return pd.DataFrame(), pd.Series()

        try:
            dataset = pd.read_csv(dataset_local_path)
        except Exception as e:
            print(f"Error loading dataset: {e}")
            return pd.DataFrame(), pd.Series()

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

    def evaluate_model(self, model, X_test, y_test):
        """
        Evaluates the model using specified metrics.

        Args:
            model (sklearn.base.BaseEstimator): The trained machine learning model.
            X_test (pd.DataFrame): Test data features.
            y_test (pd.Series): Test data labels.

        Returns:
            dict: A dictionary containing evaluation scores for the chosen metrics, or None if an error occurs.
        """
        evaluator = em.MetricsEvaluator()
        predictions = model.predict(X_test)
        evaluation_scores = {}

        for metric in self.request.evaluation_metrics:
            score = evaluator.calculate_metric(metric, y_test, predictions)
            if score is not None:
                evaluation_scores[metric] = score
            else:
                print(f"Unable to calculate metric '{metric}'.")

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
        X_train, y_train = self.load_dataset(path='TRAIN')
        X_test, y_test = self.load_dataset(path='TEST')

        model_type = self.request.task_type
        # Load hyperparameters and model type from the specified JSON file
        try:
            with open(self.request.hyperparams_path, 'r') as hp_file:
                model_config = json.load(hp_file)
        except FileNotFoundError:
            print(f"Hyperparameters file not found: {self.request.hyperparams_path}")
            return
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {self.request.hyperparams_path}")
            return

        hyperparams = model_config.get('hyperparameters', {})

        model_registry_dict = {}
        if model_type == 'classification':
            model_registry_dict = model_registry.classification_models
        elif model_type == 'regression':
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
                print(f"Model '{model_name}' not found in {model_type} registry.")
                continue

        return results