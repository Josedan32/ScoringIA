from utils.procesData import proces_data
from sklearn.base import BaseEstimator, TransformerMixin

class PrepararDatosTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return proces_data(X)