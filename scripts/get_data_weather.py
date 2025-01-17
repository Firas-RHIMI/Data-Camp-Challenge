# -*- coding: utf-8 -*-

# scrap weather data from https://freemeteo.fr/

import pandas as pd 
import numpy as np 
from get_data import *
 
raw_data_train = get_bike_data() # train data
raw_data_test = get_bike_data(test=True) # test data 
train_dates = np.sort(list(set(raw_data_train['Start Time'].apply(lambda x:x[0:10])))) # dates in train
test_dates = np.sort(list(set(raw_data_test['Start Time'].apply(lambda x:x[0:10])))) # dates in test
dates = train_dates + test_dates  
weather=pd.DataFrame()
path = 'Data/Weather/weather.csv'
    
# Function to scrap 

def scrap(data,dates):
    for date in dates:
        url = 'https://freemeteo.fr/letemps/new-york/historique/historique-quotidien/?gid=5128581&station=19438&date='+date+'&language=french&country=us-united-states'
        d = pd.read_html(url)[6]
        d = d.drop(['Rafales de Vent','Point de Rosée','Pression','Icône','DéscriptionDétails'],axis=1)
        d['Date'] = date
        data = pd.concat((data,d),ignore_index=True)
    return data 

def scrap_and_save(data,dates,path): #scraping and saving the csv files
    data = scrap(data,dates)
    data.rename(columns= {'Heure':'Hour','Température':'Temperature','Température apparente':
        'Apparent Temperature','Vent':'Wind','Humidité rel.':'Relative Humidity'},inplace=True)
    data.to_csv(path,index=False)
        
scrap_and_save(weather,dates,path)
