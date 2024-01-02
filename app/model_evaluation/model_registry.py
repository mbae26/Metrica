import logging

from sklearn.linear_model import LogisticRegression, LinearRegression, Lasso
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, RandomForestRegressor, GradientBoostingRegressor
from keras.models import Sequential
from keras.layers import Dense

class ShallowNeuralNetwork:
    """Class to create a simple shallow neural network for classification."""

    @staticmethod
    def create_classification(input_shape, **kwargs):
        """Creates and compiles a shallow neural network for classification.

        Args:
            input_shape (tuple): The shape of the input data.
            **kwargs: Additional keyword arguments for model compilation.

        Returns:
            keras.models.Sequential: A compiled Keras sequential model.
        """
        try:
            model = Sequential()
            model.add(Dense(10, activation='relu', input_shape=input_shape))
            model.add(Dense(10, activation='relu'))
            model.add(Dense(1, activation='sigmoid'))
            model.compile(optimizer=kwargs.get('optimizer', 'adam'),
                        loss=kwargs.get('loss', 'binary_crossentropy'),
                        metrics=kwargs.get('metrics', ['accuracy']))
            return model
        except Exception as e:
            logging.error("Error in creating classification model: %s", e)
            raise ValueError("Invalid input shape for classification model.") from e

    @staticmethod
    def create_regression(input_shape, **kwargs):
        """Creates and compiles a shallow neural network model for regression.

        Args:
            input_shape (tuple): The shape of the input data.
            **kwargs: Additional keyword arguments for model compilation.

        Returns:
            keras.models.Sequential: A compiled Keras sequential model.
        """
        try:
            model = Sequential()
            model.add(Dense(10, activation='relu', input_shape=input_shape))
            model.add(Dense(10, activation='relu'))
            model.add(Dense(1, activation='linear'))  # Output layer for regression
            model.compile(optimizer=kwargs.get('optimizer', 'adam'),
                        loss=kwargs.get('loss', 'mean_squared_error'),
                        metrics=kwargs.get('metrics', ['mean_squared_error']))
            return model
        except Exception as e:
            logging.error("Error in creating regression model: %s", e)
            raise ValueError("Invalid input shape for regression model.") from e


CLASSIFICATION_MODELS = {
    'LogisticRegression': LogisticRegression,
    'DecisionTree_Classification': DecisionTreeClassifier,
    'RandomForest_Classification': RandomForestClassifier,
    'AdaBoost': AdaBoostClassifier,
    'ShallowNN_Classification': ShallowNeuralNetwork.create_classification,
}

REGRESSION_MODELS = {
    'LinearRegression': LinearRegression,
    'LassoRegression': Lasso,
    'DecisionTree_Regression': DecisionTreeRegressor,
    'RandomForest_Regression': RandomForestRegressor,
    'GradientBoosting_Regression': GradientBoostingRegressor,
    'ShallowNN_Regression': ShallowNeuralNetwork.create_regression,
}
