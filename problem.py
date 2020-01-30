import os
import numpy as np
import pandas as pd
import rampwf as rw
from rampwf.workflows import FeatureExtractorRegressor
from rampwf.score_types.base import BaseScoreType
from sklearn.model_selection import GroupShuffleSplit


problem_title = 'Prediction of NYC bike sharing service usage per station'
_target_column_name = 'Surplus' 
# A type (class) which will be used to create wrapper objects for y_pred
Predictions = rw.prediction_types.make_regression()
# An object implementing the workflow

class BikeSharing(FeatureExtractorRegressor):
    def __init__(self, workflow_element_names=[
            'feature_extractor', 'regressor', 'weather.csv.zip']):
        super(BikeSharing, self).__init__(workflow_element_names[:2])
        self.element_names = workflow_element_names

workflow = BikeSharing()

# define the score (specific score for the FAN problem)
class PinballLoss(BaseScoreType):
    
    is_lower_the_better = True
    def __init__(self, name='pinball loss', precision=2):
        self.name = name
        self.precision = precision
        self.tau = 0.3

    def __call__(self, y_true, y_pred):
        if isinstance(y_true, pd.Series):
            y_true = y_true.values
        
        vals = np.maximum(- (1 - self.tau) * (y_pred - y_true), self.tau * (y_pred - y_true))
        loss = np.mean(vals)
        return loss

score_types = [
    PinballLoss(name='pinball loss', precision=2),
]

def get_cv(X, y):
    cv = GroupShuffleSplit(n_splits=8, test_size=0.20, random_state=42)
    return cv.split(X,y, groups=X['Station ID'])

def _read_data(path, f_name):
    data = pd.read_csv(os.path.join(path, 'data', f_name), low_memory=False ,compression='zip')
    y_array = data[_target_column_name].values
    X_df = data.drop(_target_column_name, axis=1)
    return X_df, y_array

def get_train_data(path='.'):
    f_name = 'train/flow_data.csv.zip'
    return _read_data(path, f_name)

def get_test_data(path='.'):
    f_name = 'test/flow_data.csv.zip'
    return _read_data(path, f_name)