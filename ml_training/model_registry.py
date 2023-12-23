from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from keras.models import Sequential
from keras.layers import Dense

class ShallowNeuralNetwork:
    """Class to create a simple shallow neural network for classification."""

    @staticmethod
    def create(input_shape, **kwargs):
        """Creates and compiles a shallow neural network model.

        Args:
            input_shape (tuple): The shape of the input data.
            **kwargs: Additional keyword arguments for model compilation.

        Returns:
            keras.models.Sequential: A compiled Keras sequential model.
        """
        model = Sequential()
        model.add(Dense(10, activation='relu', input_shape=input_shape))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(optimizer=kwargs.get('optimizer', 'adam'), 
                      loss=kwargs.get('loss', 'binary_crossentropy'), 
                      metrics=kwargs.get('metrics', ['accuracy']))
        return model

model_registry = {
    'LogisticRegression': LogisticRegression,
    'NaiveBayes': MultinomialNB,
    'DecisionTree': DecisionTreeClassifier,
    'RandomForest': RandomForestClassifier,
    'AdaBoost': AdaBoostClassifier,
    'ShallowNN': ShallowNeuralNetwork.create,
}