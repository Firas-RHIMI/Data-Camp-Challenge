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
    
    def transform(self,X_df):
        path = os.path.dirname(__file__)
        weather = pd.read_csv(os.path.join(path, 'weather.csv.zip'))
        
        def process_date(X):
            return np.c_[X['Year'], X['Month'], X['Day'],X['Hour']]
        date_transformer = FunctionTransformer(process_date, validate=False)
        
        def process_station(X):
            return np.c_[X['Station ID'], X['Longitude'], X['Latitude']]
        station_transformer = FunctionTransformer(process_station, validate=False)

        def process_weather(X):
            date = pd.to_datetime(weather['Date'],format='%Y-%m-%d')
            weather['Year'] = date.dt.year
            weather['Month'] = date.dt.month
            weather['Day'] = date.dt.day
            weather['Hour'] = pd.to_datetime(weather['Hour'], format='%H:%M').dt.hour
            weather.drop_duplicates(subset =['Hour','Day','Month','Year'],keep = 'first',inplace=True) 
            def process_wind(x):
                if 'Rafales de Vent' in x:
                    return 2 # high value
                elif 'Calme' in x:
                    return 0 # low value
                else:
                    return 1 # medium value
            weather['Wind'] = weather['Wind'].apply(process_wind)
            weather['Apparent Temperature'] = (weather['Apparent Temperature'].str[:-2]).astype(float)
            weather['Temperature'] = (weather['Temperature'].str[:-2]).astype(float)
            weather['Relative Humidity'] = (weather['Relative Humidity'].str[:-1]).astype(float)
            df = pd.merge(X, weather, on=['Year', 'Month', 'Day', 'Hour'], how='left', left_index=True)
            return df[['Temperature', 'Apparent Temperature', 'Wind', 'Relative Humidity']] 

        
        weather_transformer = FunctionTransformer(process_weather, validate=False)


        date_cols = ['Year', 'Month', 'Day','Hour']
        station_cols = ['Station ID', 'Longitude', 'Latitude']
        merge_col = ['Year', 'Month', 'Day', 'Hour']
        drop_cols = ['Station Name']

        self.preprocessor = ColumnTransformer(
            transformers=[
                ('weather', make_pipeline(weather_transformer, SimpleImputer(strategy='median')), merge_col),
                ('station', make_pipeline(station_transformer, SimpleImputer(strategy='median')), station_cols),
                ('date', make_pipeline(date_transformer, SimpleImputer(strategy='median')), date_cols),
                ('drop cols', 'drop', drop_cols)
            ])

        
        X_array = self.preprocessor.fit_transform(X_df)
        return X_array
