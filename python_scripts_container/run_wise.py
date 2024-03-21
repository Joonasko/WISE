#!/usr/bin/python3
# import modules
print('running run_wise.py')
import sys
import argparse
import os
import xarray as xr
import subprocess
import csv

# defining file input / output paths
in_path = '/input_data/'
out_path = '/input_data/'

# reading the run dates file
#with open('/testjobs/run_dates.txt', 'r') as file:
#    lines = file.read().splitlines()

# using the environment variable to get run dates
dates_str = os.getenv('ALL_DATES')
print(dates_str)
if dates_str:
      year_start, month_start, day_start, year_end, month_end, day_end = dates_str.split(',')
else:
    print("Environment variable 'ALL_DATES' not found or is invalid.")
    sys.exit(1)
    
# taking the start and end dates from the dates file
#year_start = str(lines[0])
#year_end = str(lines[1])
#month_start = str(lines[2])
#month_end = str(lines[3])
#day_start = str(lines[4])
#day_end = str(lines[5])

# Provide the data file name for all variables (weekly)
temp_name = f'{year_start}_{month_start}_{day_start}_T00_to_{year_end}_{month_end}_{day_end}_T23_2t_hourly_mean.nc' # temperature
dewpoint_name = f'{year_start}_{month_start}_{day_start}_T00_to_{year_end}_{month_end}_{day_end}_T23_2d_hourly_mean.nc' # dewpoint temperature
uwind_name  = f'{year_start}_{month_start}_{day_start}_T00_to_{year_end}_{month_end}_{day_end}_T23_10u_hourly_mean.nc' # u wind
vwind_name  = f'{year_start}_{month_start}_{day_start}_T00_to_{year_end}_{month_end}_{day_end}_T23_10v_hourly_mean.nc' # v wind
precip_name    = f'{year_start}_{month_start}_{day_start}_T00_to_{year_end}_{month_end}_{day_end}_T23_tp_hourly_mean.nc' # precipitation

# read the netcdf files and take variables
temp_nc = xr.open_dataset(in_path+temp_name)
dewpoint_nc = xr.open_dataset(in_path+dewpoint_name)
windu_nc = xr.open_dataset(in_path+uwind_name)
windv_nc = xr.open_dataset(in_path+vwind_name)
precip_nc = xr.open_dataset(in_path+precip_name)

windu_var = windu_nc['10u']
windv_var = windv_nc['10v']
temp_var = temp_nc['2t']
dewpoint_var = dewpoint_nc['2d']
precip_var = precip_nc['tp']

# combine all variables into singular file
combined_nc = xr.Dataset({
    '10u': windu_var,
    '10v': windv_var,
    '2t': temp_var,
    '2d': dewpoint_var,
    'tp': precip_var,
})

file_name = out_path+'combined_ncdf.nc'

# write the new netcdf file
combined_nc.to_netcdf(file_name)

# current working dir
current_directory = os.getcwd()

# get the group id
directory_stat = os.stat(current_directory)

# get group ownership
group_owner_gid = directory_stat.st_gid

parent_directory = os.path.dirname(file_name)
parent_gid = os.stat(parent_directory).st_gid

# change group ownership
os.chown(file_name, -1, parent_gid)


# run the ncdf_edits_multiarea.py script
cmd = ['python3','/python_scripts/ncdf_edits_multiarea.py']
print('staring ncdf_edits_multiarea.py')
subprocess.run(cmd + [out_path+'combined_ncdf.nc'])

# run the WISE model for the three test areas in Finland
print('launching WISE runs')
cmd = ['wise','-r', '4', '-f', '0', '-t', '/testjobs/testjobs/area1/job.fgmj']
subprocess.run(cmd)
cmd = ['wise','-r', '4', '-f', '0', '-t', '/testjobs/testjobs/area2/job.fgmj']
subprocess.run(cmd)
cmd = ['wise','-r', '4', '-f', '0', '-t', '/testjobs/testjobs/area3/job.fgmj']
subprocess.run(cmd)
