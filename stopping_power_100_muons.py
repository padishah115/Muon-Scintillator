import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import simulation_package.lifetime_processing as life

current_directory = 'C:\\Users\\hayde\\Desktop\\Muon Scintillator\\stop_and_pop_data_100\\stops'
entries = os.listdir(current_directory)
files = [f for f in entries if os.path.isfile(os.path.join(current_directory, f))]
files_csv = []
files_sanitised = []

energy_ranges = []
stop_percents = []

for file in files:
    if '.csv' in file:
        df = pd.read_csv('C:\\Users\\hayde\\Desktop\\Muon Scintillator\\stop_and_pop_data_100\\stops\\' + file)
        stops = df['stops boolean']


        print(f'File: {file}')
        print(f'Length of file: {len(stops)}')

        stop_percent = life.percentage_stopped(stops)
        print(stop_percent)
        stop_percents.append(stop_percent)  

        file_stripped = ''.join(letter for letter in file if letter.isdigit())
        
        energy_ranges.append(file_stripped)

stopping_percentage_dataframe = pd.DataFrame({
    'energy ranges' : energy_ranges,
    'percentage stopped' : stop_percents
    
    })

stopping_percentage_dataframe.to_csv('C:\\Users\\hayde\\Desktop\\Muon Scintillator\\stop_and_pop_data_100\\stops\\stopping_percentages_100_muons.csv', index=False)
