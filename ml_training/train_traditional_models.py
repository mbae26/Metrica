import os
import argparse
import json
import joblib
import pandas as pd

from model_registry import model_registry

class ModelTrainer:
    """Handles the training and saving of traditional machine learning models.

    Attributes:
        save_path (str): Directory path where trained models will be saved.
    """

    def __init__(self, save_path):
        """Inits ModelTrainer with the path where models will be saved."""
        self.save_path = save_path

    def load_dataset(self, dataset_name):
        """Loads and returns the dataset for training.

        Placeholder function to be replaced when integrating with S3

        Args:
            dataset_name (str): The name or path of the dataset to load.

        Returns:
            Tuple[pd.DataFrame, pd.Series]: A tuple containing the training data features and labels (X_train, y_train).
        """
        pass  # Implement dataset loading logic here

    def train_model(self, model_name, model, X_train, y_train):
        """Trains a model and saves it.

        Trains the given model on the training dataset and then saves it to disk.

        Args:
            model_name (str): The name of the model.
            model (sklearn.base.BaseEstimator): The machine learning model to train.
            X_train (pd.DataFrame): Training data features.
            y_train (pd.Series): Training data labels.
        """
        print(f'Training {model_name}...')
        model.fit(X_train, y_train)
        self.save_model(model, model_name)

    def save_model(self, model, model_name):
        """Saves the trained model to disk.

        Args:
            model (sklearn.base.BaseEstimator): The trained machine learning model.
            model_name (str): The name of the model.
        """
        model_save_path = os.path.join(self.save_path, f"{model_name}.joblib")
        joblib.dump(model, model_save_path, compress=True)


def main(args):
    trainer = ModelTrainer(save_path=os.path.join('.', args.key, 'traditional_models'))
    os.makedirs(trainer.save_path, exist_ok=True)

    X_train, y_train = trainer.load_dataset(args.dataset)

    # Load hyperparameters from the specified JSON file
    try:
        with open(args.hyperparams, 'r') as hp_file:
            hyperparams = json.load(hp_file)
    except FileNotFoundError:
        print(f"Hyperparameters file not found: {args.hyperparams}")
        return
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {args.hyperparams}")
        return

    for model_name, params in hyperparams.items():
        if model_name in model_registry:
            model = model_registry[model_name](**params)
            trainer.train_model(model_name, model, X_train, y_train)
        else:
            print(f"Model \'{model_name}\' not found in registry.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', type=str, default='00000000')
    parser.add_argument('--dataset', type=str, required=True)
    parser.add_argument('--hyperparams', type=str, required=True, help="Path to JSON file with model names and hyperparameters")
    args = parser.parse_args()
    main(args)
