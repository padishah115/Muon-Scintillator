import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import simulation_package.lifetime_processing as life

current_directory = 'C:\\Users\\hayde\\Desktop\\Muon Scintillator\\stop_and_pop_data_100\\'
entries = os.listdir(current_directory)
files = [f for f in entries if os.path.isfile(os.path.join(current_directory, f))]
files_csv = []
files_sanitised = []


for file in files:
    if 'stopping_percentages_100_muons.csv' in file:
        df = pd.read_csv('C:\\Users\\hayde\\Desktop\\Muon Scintillator\\stop_and_pop_data_100\\' + file)


        print(f'File: {file}')

        energy_ranges = df['energy ranges']
        stop_percentages = df['percentage stopped']

        print(len(energy_ranges))
        print(len(stop_percentages))


plt.bar(energy_ranges, stop_percentages)
plt.title('Percentage of Muons Stopped for \n 100 Generated Muons in Various Energy Ranges')
plt.ylabel('Percentage Stopped / %')
plt.xlabel('Energy Range / Mev')
plt.xticks(rotation = 90)
plt.ylim(0,100)
plt.show()


 

