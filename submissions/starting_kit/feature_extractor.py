import os
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline


class FeatureExtractor(object):
    def __init__(self):
        pass

    def fit(self, X_df, y_array):
        return self

    def transform(self, X_df):

#         path = os.path.dirname(__file__)
#         weather = pd.read_csv(os.path.join(path, 'Data/Weather Data/Train_Weather.csv'))

        def process_date(X):
            return np.c_[X['Year'], X['Month'], X['Day']]
        date_transformer = FunctionTransformer(process_date, validate=False)
        
        def process_station(X):
            return np.c_[X['Station ID'], X['Longitude'], X['Latitude']]
        station_transformer = FunctionTransformer(process_station, validate=False)

        def process_weather(X):
            date = pd.to_datetime(weather['Date'], format='%Y-%m-%d')
            weather['Year'] = date.dt.year
            weather['Month'] = date.dt.month
            weather['Day'] = date.dt.day
            weather['Hour'] = pd.to_datetime(weather['Hour'], format='%H:%M').dt.hour
            df = pd.merge(X, weather, on=['Year', 'Month', 'Day', 'Hour'], how='inner')
            df['Temperature'] = df['Temperature'].str[:-2]
            df['Apparent Temperature'] = df['Apparent Temperature'].str[:-2]
            print(X.shape, weather.shape, df.shape)
            return df[['Temperature', 'Apparent Temperature']] #, 'Wind', 'Relative Humidity']]        
        weather_transformer = FunctionTransformer(process_weather, validate=False)


        date_cols = ['Year', 'Month', 'Day']
        station_cols = ['Station ID', 'Longitude', 'Latitude']
        merge_col = ['Year', 'Month', 'Day', 'Hour']

        preprocessor = ColumnTransformer(
            transformers=[
#                 ('weather', make_pipeline(weather_transformer, SimpleImputer(strategy='median')), merge_col),
                ('date', make_pipeline(date_transformer, SimpleImputer(strategy='median')), date_cols),
                ('station', make_pipeline(station_transformer, SimpleImputer(strategy='median')), station_cols),
            ])

        X_array = preprocessor.fit_transform(X_df)
        return X_array
