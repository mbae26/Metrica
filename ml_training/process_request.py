import os
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, mean_squared_error
import model_registry


class RequestProcessor:
    def __init__(self, request, s3_client, save_path):
        """Initializes RequestProcessor with request, S3 client, and save path."""
        self.request = request
        self.s3_client = s3_client
        self.save_path = save_path

    def process_request(self):
        """Processes the request by training and evaluating models."""
        X_train, y_train = self.load_dataset()
        results = {}

        # Choose the right model registry based on task type
        model_registry_dict = model_registry.classification_models if self.request.task_type == 'CLASSIFICATION' else model_registry.regression_models

        for model_name, model_class in model_registry_dict.items():
            model = model_class()
            self.train_model(model_name, model, X_train, y_train)
            score = self.evaluate_model(model, X_train, y_train)
            results[model_name] = score

        return results

    def load_dataset(self):
        """Loads the dataset from S3 and returns training data and labels."""
        dataset_file_name = f"train/{self.request.user_id}_{self.request.submission_time}.csv"
        dataset_local_path = os.path.join('datasets', dataset_file_name)

        self.s3_client.download_file(dataset_file_name, dataset_local_path)
        dataset = pd.read_csv(dataset_local_path)
        X_train = dataset.iloc[:, :-1]
        y_train = dataset.iloc[:, -1]
        return X_train, y_train

    def train_model(self, model_name, model, X_train, y_train):
        """Trains the model and saves it."""
        print(f'Training {model_name}...')
        model.fit(X_train, y_train)
        self.save_model(model, model_name)

    def evaluate_model(self, model, X_train, y_train):
        """Evaluates the model and returns the score."""
        predictions = model.predict(X_train)
        if self.request.task_type == 'CLASSIFICATION':
            # MORE EVALUATION METRICS/LOGIC HERE
            return accuracy_score(y_train, predictions)
        else:
            return mean_squared_error(y_train, predictions)

    def save_model(self, model, model_name):
        """Saves the trained model to disk."""
        model_save_path = os.path.join(self.save_path, f"{model_name}.joblib")
        joblib.dump(model, model_save_path, compress=True)
        print(f"Saved {model_name} model to {model_save_path}")
