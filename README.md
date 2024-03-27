# WISE
This repository does the required climate data edits to be used in the Canadian forest fire spread model WISE. Hourly values are transformed from netcdf files to a singular .txt file for each of the 3 test areas in Finland. The required job.fgmj files for running WISE are then edited based on the temporal extent of the weather files and ignition locations.

Instructions on required packages and how to use the code are provided below.

Required python modules:
sys
argparse
os
subprocess
csv

Installation:
No installation is required as the application is installed in a singularity container located in LUMI. The container takes the python scripts (python_scripts_container) as input and uses them to run both input data editing and handles the model runs.

How to run:
start and end times will be defined by the workflow, e.g.:
python run_wildfires_wise.py -year_start 2021 -year_end 2021 -month_start 06 -month_end 06 -day_start 24 -day_end 30 -expid a0c1

The run_wildfires_wise.py will take the start and end dates as input and select the correct netcdf files based on this. Next the required input and output directories will be binded to the singularity container, after which it will be run from the run_wildfires_wise.py script. In the container the run_wise.py will first select the correct netcdf files and combine them into a singular file. The ncdf_edits_multiarea.py will take this combined ncdf file and select the closest cell to each ignition location, make the necessary transformation and calculations and create the weather files (weather.txt) for each of the three scenarios. Next the modify_fgmj.py will make the required alterations to the job.fgmj files which WISE uses for model run setting. Finally, the run_wildfires_wise.py will run the WISE model for the three different scenarios. Application output consists of raster, vector and text files. The daily run results are divided into separate folders based on the test area, run start time and the date used for the model run, e.g. scen_lieksa_2024-03-26_22_31_2000-08-26 contains results for the Lieksa area for the date 26.8.2000 and the application was ran on 26.3.2024 at 22:31. The text (.txt) file summary contains information about the used input files, model run setting used and ignition locations. The vector (.kml) file perim contains fire propagation polygons at an hourly temporal resolution. The raster files (.tif) consist of max_crown_fraction_burned (maximum crown fraction burned in each cell, %), max_flame_length (maximum flame lenght in each cell, meters), max_intensity (maximum fire intensity in each cell, kilowats), surface_fuel_consumed (surface fuel consumption in each cell, kg), crown_fuel_consumed (crown fuel consumption in each cell, kg) and total_fuel_consumption (total fuel consumption from both canopy and surface, kg) files. The spatial resolution of the raster files is 16 x 16 m. These files are created from the last time step of the fire spread to include all values from the model run. 

Data request file:
Data request file is the request.yml file
