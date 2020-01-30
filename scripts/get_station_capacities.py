import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from get_data import *

# Stations in the dataset
raw_data = get_bike_data()
stations = set(raw_data['Start Station Name'])
stations = stations.union(set(raw_data['End Station Name']))
station_with_caps = {}

driver = webdriver.Chrome()
driver.get("https://member.citibikenyc.com/map/")
input_box = driver.find_element_by_name('bike-search')

# Search for stations in webpage
for s in stations:
    if isinstance(s, str):
        try:
            input_box.click()
            input_box.clear()
            input_box.send_keys(s)
            time.sleep(0.5)
            first_res = driver.find_element_by_class_name('ed-map-search__result_station')
            first_res.click()
            time.sleep(1)
            bikes = driver.find_element_by_class_name('ed-map__canvas__info-window__content__detail__bikes__available__val')
            docks = driver.find_element_by_class_name('ed-map__canvas__info-window__content__detail__docks__available__val')
            station_capacity = int(bikes.text) + int(docks.text)
            station_with_caps[s] = station_capacity
        except:
            print('Error with ' + s)

# Add few results where script doesn't work
station_with_caps['W Broadway & Spring Street'] = 42
station_with_caps['Cliff St & Fulton St_1'] = 37
station_with_caps['Exchange Place'] = 30

# Save file
json.dump(station_with_caps, open('../data/stations.json', 'w'))


