# -*- coding: utf-8 -*-

# Read and process Data 

import os 
import pandas as pd


train_path ='../data/train'
test_path = '../data/test'

def get_bike_data(test=False): #Get raw citibike data 
    path = test_path if test else train_path
    try:F
        data = pd.read_csv(os.path.join(path, 'bike_data.csv.zip'), low_memory=False)
    except:
        data = pd.DataFrame()
        for file in os.listdir(path):
            aux = pd.read_csv(os.path.join(path, file))
            data = pd.concat((data, aux), ignore_index=True)
        data.to_csv(os.path.join(path, 'bike_data.csv.zip'))
    return data
    
def get_flow_data(test=False): #Processes raw data and return flow data for predictions
    path = test_path if test else train_path
    try:
        data = pd.read_csv(os.path.join(path, 'flow_data.csv.zip', low_memory=False))

    except:
        data = get_bike_data(test)
        ## process time
        start=pd.to_datetime(data['Start Time'])
        data['Start Year']=start.dt.year
        data['Start Month']= start.dt.month
        data['Start Day']= start.dt.day
        data['Start Hour']= start.dt.hour
        stop= pd.to_datetime(data['Stop Time'])
        data['Stop Year']=stop.dt.year
        data['Stop Month']= stop.dt.month
        data['Stop Day']= stop.dt.day
        data['Stop Hour']= stop.dt.hour

        ## drop extra data 
        data = data.drop(columns=['Trip Duration','User Type','Birth Year','Gender','Start Time','Stop Time'])

        ## groupbys
        groupby_out_columns=['Start Year','Start Month','Start Day','Start Hour','Start Station ID','Start Station Name','Start Station Latitude','Start Station Longitude']
        data_out = data.groupby(groupby_out_columns).size().reset_index().rename(columns={0:'Out'})
        groupby_in_columns=['Stop Year','Stop Month','Stop Day','Stop Hour','End Station ID','End Station Name','End Station Latitude','End Station Longitude']
        data_in = data.groupby(groupby_in_columns).size().reset_index().rename(columns={0:'In'})

        ## merge
        merge_in_columns=['Stop Year','Stop Month','Stop Day','Stop Hour','End Station ID']
        merge_out_columns=['Start Year','Start Month','Start Day','Start Hour','Start Station ID']
        merge = pd.merge(data_in,data_out,left_on=merge_in_columns, right_on = merge_out_columns, how='outer' ).fillna(-9999)  
        merge['End Station Name'].replace(-9999,"", inplace = True)
        merge['Start Station Name'].replace(-9999,"",inplace=True)
        merge['Station ID'] = merge[['Start Station ID','End Station ID']].max(axis=1)
        merge['Longitude']=merge[['Start Station Longitude','End Station Longitude']].max(axis=1)
        merge['Latitude']=merge[['Start Station Latitude','End Station Latitude']].max(axis=1)
        merge['Year']=merge[['Start Year','Stop Year']].max(axis=1)
        merge['Month']=merge[['Start Month','Stop Month']].max(axis=1)
        merge['Day']=merge[['Start Day','Stop Day']].max(axis=1)
        merge['Hour']=merge[['Start Hour','Stop Hour']].max(axis=1)
        merge['Station Name']=merge[['Start Station Name','End Station Name']].max(axis=1)
        merge['Surplus'] = merge['In'].replace(-9999,0) - merge['Out'].replace(-9999,0)

        # columns to keep
        keep_columns=['Year','Month','Day','Hour','Station ID','Station Name','Longitude','Latitude','Surplus']
        data = merge[keep_columns]
        data.to_csv(os.path.join(path, 'flow_data.csv.zip'))

    return data






