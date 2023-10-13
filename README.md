# WISE
This repository does the required climate data edits to be used in the Canadian forest fire spread model WISE. Hourly values are transformed from netcdf files to a singular .txt file for each of the 3 test areas in Finland. The required job.fgmj files for running WISE are then edited based on the temporal extent of the weather files and ignition locations.

Instructions on required packages and how to use the code are provided below.

Required python modules:
argparse
os
xarray
subprocess
numpy
pandas
sys
datetime
json

Installation:
No installation is required as the application is installed in a singularity container located in LUMI. The container takes the python scripts (python_scripts_container) as input and uses them to run both input data editing and handles the model runs.

How to run:
# start and end times will be defined by the workflow
python run_wildfires_wise.py -year_start 2021 -year_end 2021 -month_start 06 -month_end 06 -day_start 24 -day_end 30 -expid a0c1

Data request file:
Data request file is the request.yml file
