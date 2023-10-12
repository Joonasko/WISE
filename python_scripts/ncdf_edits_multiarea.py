print('running ncdf_edits_multiarea.py')
# import required packages
import argparse
import numpy as np
import xarray as xr
import pandas as pd
import subprocess
import sys
from datetime import datetime

# load netcdf dataset
#dataset = xr.open_dataset('D:/wise/first_week2.nc')

# taking the combined ncdf file as input
ncdf_file_path = sys.argv[1]
#print(ncdf_file_path)
dataset = xr.open_dataset(ncdf_file_path)

#print('variables:')
#for var_name in dataset.variables:
#    print(var_name, dataset.variables[var_name])

#print('Dimensions:')
#for dim_name in dataset.dims:
#    print(dim_name, dataset.dims[dim_name])

#print('Global Attributes:')
#for attr_name in dataset.attrs:
#    print(attr_name, dataset.attrs[attr_name])

# calculate wind speed and direction from 10u and 10v components
wind_speed = np.sqrt(dataset['10u']**2 + dataset['10v']**2)
dataset['wind_speed'] = wind_speed

wind_direction_rad = np.arctan2(dataset['10v'],dataset['10u'])
wind_direction_deg = np.degrees(wind_direction_rad)
wind_direction_deg = (wind_direction_deg + 360) % 360
dataset['wind_direction'] = wind_direction_deg

# calculate relative humidity and convert temperatures to Celsius
temperature_celsius = dataset['2t'] - 273.15  # Convert from Kelvin to Celsius
dewpoint_celsius = dataset['2d'] - 273.15  # Convert from Kelvin to Celsius
relative_humidity = 100 * (np.exp((17.625 * dewpoint_celsius) / (243.04 + dewpoint_celsius)) / np.exp((17.625 * temperature_celsius) / (243.04 + temperature_celsius)))

dataset['relative_humidity'] = relative_humidity
dataset['temperature'] = temperature_celsius

# set the ignition coordinates for 3 areas
area1_lat = 64.007044
area1_lon = 24.152986
area2_lat = 63.429000
area2_lon = 30.545000
area3_lat = 63.040000
area3_lon = 29.990000

# select only closest cell from netcdf to each ignition location
nearest_cell1 = dataset.sel(lat=area1_lat,lon=area1_lon,method='nearest')
nearest_cell2 = dataset.sel(lat=area2_lat,lon=area2_lon,method='nearest')
nearest_cell3 = dataset.sel(lat=area3_lat,lon=area3_lon,method='nearest')

df1 = nearest_cell1.to_dataframe()
df2 = nearest_cell2.to_dataframe()
df3 = nearest_cell3.to_dataframe()

# make required dataframe edits
df1.reset_index(inplace=True)
df1.set_index('time',inplace=True)
df2.reset_index(inplace=True)
df2.set_index('time',inplace=True)
df3.reset_index(inplace=True)
df3.set_index('time',inplace=True)

df1['date'] = df1.index.date
df1['hour'] = df1.index.time
df2['date'] = df2.index.date
df2['hour'] = df2.index.time
df3['date'] = df3.index.date
df3['hour'] = df3.index.time

variables_to_drop = ['10v','10u','2t','2d']
df1 = df1.drop(variables_to_drop, axis = 1)
df2 = df2.drop(variables_to_drop, axis = 1)
df3 = df3.drop(variables_to_drop, axis = 1)

# create datetime series for scenario start and end times (start at each day 10:00 and end same day 21:00)
combined_datetime_series = pd.to_datetime(df1.index.date) + pd.to_timedelta([time.hour for time in df1.index], unit='h')

combined_datetime_series = pd.Series(combined_datetime_series)

dates_at_10 = combined_datetime_series[combined_datetime_series.apply(lambda x: x.time() == pd.to_datetime('10:00:00').time())]
dates_at_21 = combined_datetime_series[combined_datetime_series.apply(lambda x: x.time() == pd.to_datetime('21:00:00').time())]

dates_at_10 = dates_at_10.apply(lambda x: x.strftime('%Y-%m-%dT%H:%M:%S'))
dates_at_21 = dates_at_21.apply(lambda x: x.strftime('%Y-%m-%dT%H:%M:%S'))

df1.reset_index(inplace=True)
df2.reset_index(inplace=True)
df3.reset_index(inplace=True)

# set column order
new_column_order = ['date', 'hour', 'temperature', 'relative_humidity', 'wind_direction', 'wind_speed', 'tp']
df1 = df1[new_column_order]
df2 = df2[new_column_order]
df3 = df3[new_column_order]

# Rename the columns
df1.rename(columns={
    'date': 'HOURLY',
    'hour': 'HOUR',
    'temperature': 'TEMP',
    'relative_humidity': 'RH',
    'wind_direction': 'WD',
    'wind_speed': 'WS',
    'tp': 'PRECIP',
}, inplace=True)

df2.rename(columns={
    'date': 'HOURLY',
    'hour': 'HOUR',
    'temperature': 'TEMP',
    'relative_humidity': 'RH',
    'wind_direction': 'WD',
    'wind_speed': 'WS',
    'tp': 'PRECIP',
}, inplace=True)

df3.rename(columns={
    'date': 'HOURLY',
    'hour': 'HOUR',
    'temperature': 'TEMP',
    'relative_humidity': 'RH',
    'wind_direction': 'WD',
    'wind_speed': 'WS',
    'tp': 'PRECIP',
}, inplace=True)

# Convert 'date' to datetime format
df1['HOURLY'] = pd.to_datetime(df1['HOURLY'], format='%d/%m/%Y')
df2['HOURLY'] = pd.to_datetime(df2['HOURLY'], format='%d/%m/%Y')
df3['HOURLY'] = pd.to_datetime(df3['HOURLY'], format='%d/%m/%Y')

# Convert 'hour' to integers
df1['HOUR'] = df1['HOUR'].apply(lambda x: x.hour).astype(int)
df2['HOUR'] = df2['HOUR'].apply(lambda x: x.hour).astype(int)
df3['HOUR'] = df3['HOUR'].apply(lambda x: x.hour).astype(int)

# Round all values to one decimal place
df1 = df1.round(1)
df2 = df2.round(1)
df3 = df3.round(1)

# Format the 'date' column as 'dd/mm/yyyy'
df1['HOURLY'] = df1['HOURLY'].dt.strftime('%d/%m/%Y')
df2['HOURLY'] = df2['HOURLY'].dt.strftime('%d/%m/%Y')
df3['HOURLY'] = df3['HOURLY'].dt.strftime('%d/%m/%Y')

# save the new .txt format weather files to their designated job folders for WISE runs

#file_path = '/mnt/d/wise/wise_area_data/testjobs/'
file_path = '/projappl/project_465000454/kolstela/wise_lumi/testjobs/'
df1.to_csv((f'{file_path}area1/Inputs/weather.txt'), sep =',', index =False)
df2.to_csv((f'{file_path}area2/Inputs/weather.txt'), sep =',', index =False)
df3.to_csv((f'{file_path}area3/Inputs/weather.txt'), sep =',', index =False)

cmd = ['python3','/scratch/project_465000454/kolstela/a0c1/workflow/wildfires_wise/python_scripts/ncdf_edits_multiarea.py']
#cmd = ['python3','/mnt/d/wise/wise_git_working/WISE/python_scripts/modify_fgmj.py']
arguments = [str(dates_at_10),str(dates_at_21),str(area1_lat),str(area1_lon),str(area2_lat),str(area2_lon),str(area3_lat),str(area3_lon)]
print('ncdf_edits_multiarea.py done, starting modify_fgmj.py')
subprocess.run(cmd + arguments)
