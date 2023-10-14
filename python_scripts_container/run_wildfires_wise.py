# import modules
print('running run_wildfires.py')
import sys
import argparse
import os
import subprocess
import csv

# parser etc. to be added in application integration

# creating the parser
#parser = argparse.ArgumentParser(description='Runscript for data notifier job.')

# adding year, month and day arguments
#parser.add_argument('-year_start', required=True, help='Input year', default=1)
#parser.add_argument('-month_start', required=True, help='Input month', default=2)
#parser.add_argument('-day_start', required=True, help='Input day', default=3)

#parser.add_argument('-year_end', required=True, help='Input year', default=4)
#parser.add_argument('-month_end', required=True, help='Input month', default=5)
#parser.add_argument('-day_end', required=True, help='Input day', default=6)

# parsing the arguments
#args = parser.parse_args()
#year_start = str(args.year_start)
#month_start = str(args.month_start)
#day_start = str(args.day_start)
#year_end = str(args.year_end)
#month_end = str(args.month_end)
#day_end = str(args.day_end)

# placeholder values for manual runs
year_start = "2020"
year_end = "2020"
month_start = "06"
month_end = "06"
day_start = "24"
day_end = "30"

# create .txt file with start and end dates
all_dates = [year_start,year_end,month_start,month_end,day_start,day_end]

with open('/projappl/project_465000454/kolstela/wise_lumi_container/wise_lumi_files/run_dates.txt', 'w') as file:
    for element in all_dates:
        file.write(element + '\n')


print("Data written to 'formatted_data.txt'")

# build the command for running the singularity container wise.sif
cmd = [
    'singularity',
    'run',
    '--bind', '/projappl/project_465000454/kolstela/wise_lumi_container/wise_lumi_files:/testjobs',
    '--bind', '/scratch/project_465000454/kolstela/a0c1/workflow/wildfires_wise/python_scripts_container:/python_scripts',
    '--bind', '/projappl/project_465000454/kolstela/wise_lumi_container/wise_outputs:/testjobs/testjobs/area1/Outputs',
    '--bind', '/projappl/project_465000454/kolstela/wise_lumi_container/wise_outputs:/testjobs/testjobs/area2/Outputs',
    '--bind', '/projappl/project_465000454/kolstela/wise_lumi_container/wise_outputs:/testjobs/testjobs/area3/Outputs',
    '--bind', '/scratch/project_465000454/tmp/a0c1:/input_data',
    '/projappl/project_465000454/kolstela/wise_lumi_container/wise.sif'
]

# run the container wise.sif
print('launching WISE runs')
subprocess.run(cmd)

