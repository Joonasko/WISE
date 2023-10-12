print('running run_wildfires.py')
import argparse
import os
import xarray as xr
import subprocess


# parser etc. to be added in application integration

# creating the parser
#parser = argparse.ArgumentParser(description='Runscript for data notifier job.')

# adding year, month and day arguments
#parser.add_argument('-year', required=True, help='Input year', default=1)
#parser.add_argument('-month', required=True, help='Input month', default=2)
#parser.add_argument('-day', required=True, help='Input day', default=3)

# parsing the arguments
#args = parser.parse_args()
#year = args.year
#month = args.month
#day = args.day

# defining file input / output paths
in_path = '/scratch/project_465000454/tmp/a0c1/'
out_path = '/scratch/project_465000454/kolstela/'
#in_path = '/mnt/d/wise/testset_1/'
#out_path = '/mnt/d/wise/testset_1/'


year = '2021'
month = '06'
day = '24'



# Provide the data file name for all variables
temp_name = f'{year}_{month}_{day}_T00_00_to_{year}_{month}_{day}_T23_00_2t_hourly_raw.nc' # temperature
dewpoint_name = f'{year}_{month}_{day}_T00_00_to_{year}_{month}_{day}_T23_00_2d_hourly_raw.nc' # dewpoint temperature
uwind_name  = f'{year}_{month}_{day}_T00_00_to_{year}_{month}_{day}_T23_00_10u_hourly_raw.nc' # u wind
vwind_name  = f'{year}_{month}_{day}_T00_00_to_{year}_{month}_{day}_T23_00_10v_hourly_raw.nc' # v wind
precip_name    = f'{year}_{month}_{day}_T00_00_to_{year}_{month}_{day}_T23_00_tp_hourly_raw.nc' # precipitation
#out_name    = f'WISE_{year}_{month}_{day}_output.nc'
#ct_name     = 'WISE_Const.nc'

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

combined_nc = xr.Dataset({
    '10u': windu_var,
    '10v': windv_var,
    '2t': temp_var,
    '2d': dewpoint_var,
    'tp': precip_var,
})

combined_nc.to_netcdf(out_path+'combined_ncdf.nc')

cmd = ['python3','/scratch/project_465000454/kolstela/a0c1/workflow/wildfires_wise/python_scripts/ncdf_edits_multiarea.py']
#cmd = ['python3','/mnt/d/wise/wise_git_working/WISE/python_scripts/ncdf_edits_multiarea.py']
print('staring ncdf_edits_multiarea.py')
subprocess.run(cmd + [out_path+'combined_ncdf.nc'])

print('launching WISE runs')
cmd = ['sh','/projappl/project_465000454/kolstela/wise_lumi/full_run_kalajoki.sh']
subprocess.run(cmd)
cmd = ['sh','/projappl/project_465000454/kolstela/wise_lumi/full_run_koli.sh']
subprocess.run(cmd)
cmd = ['sh','/projappl/project_465000454/kolstela/wise_lumi/full_run_lieksa.sh']
subprocess.run(cmd)
