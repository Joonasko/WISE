#!/usr/bin/python3
# import modules
print('running .fgmj modifier')
import os
import sys
import json
from datetime import datetime

# take the time and ignition lat lon variables
scenario_start = sys.argv[1]
scenario_end = sys.argv[2]
ignition_start = sys.argv[3]
ignition_end = sys.argv[4]
ignition_y_1 = float(sys.argv[5])
ignition_x_1 = float(sys.argv[6])
ignition_y_2 = float(sys.argv[7])
ignition_x_2 = float(sys.argv[8])
ignition_y_3 = float(sys.argv[9])
ignition_x_3 = float(sys.argv[10])

# set scenario names
scen_name_1 = 'scen_kalajoki'
scen_name_2 = 'scen_koli'
scen_name_3 = 'scen_lieksa'

# set input fgmj path and read the fgmj files
fgmj_path = '/testjobs/testjobs/job.fgmj'


with open(fgmj_path, 'r') as f:
    fgmj_data1 = json.load(f)

with open(fgmj_path, 'r') as f:
    fgmj_data2 = json.load(f)

with open(fgmj_path, 'r') as f:
    fgmj_data3 = json.load(f)

# set variables
scenario_start = ignition_start
scenario_end = scenario_end
local_start_time = ignition_start
start_time = ignition_start
end_time = scenario_end
ignition_start = ignition_start
output_time = scenario_end

# function for replacing values in dictionary
def replace_in_dict(data, find, replace):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                replace_in_dict(value, find, replace)
            elif isinstance(value, str):
                data[key] = value.replace(find, replace)

    elif isinstance(data, list):
        for index, value in enumerate(data):
            if isinstance(value, (dict, list)):
                replace_in_dict(value, find, replace)
            elif isinstance(value, str):
                data[index] = value.replace(find, replace)

# function for editing the job.fgmj files
def create_job(data_in, job_name, scen_name, ign_lon, ign_lat):

    data_in['project']['scenarios']['scenarioData'][0]['startTime']['time'] = scenario_start

    data_in['project']['scenarios']['scenarioData'][0]['endTime']['time'] = scenario_end

    data_in['project']['scenarios']['scenarioData'][0]['temporalConditions']['daily'][0]['localStartTime']['time'] = local_start_time

    data_in['project']['scenarios']['scenarioData'][0]['temporalConditions']['daily'][0]['startTime']['time'] = start_time

    data_in['project']['scenarios']['scenarioData'][0]['temporalConditions']['daily'][0]['endTime']['time'] = end_time

    data_in['project']['ignitions']['ignitionData'][0]['startTime']['time'] = ignition_start

    data_in['project']['ignitions']['ignitionData'][0]['ignitions']['ignitions'][0]['polygon']['polygon']['points'][0]['x']['value'] = ign_lon

    data_in['project']['ignitions']['ignitionData'][0]['ignitions']['ignitions'][0]['polygon']['polygon']['points'][0]['y']['value'] = ign_lat

    data_in['project']['outputs']['grids'][0]['exportTime']['time'] = output_time

    data_in['project']['outputs']['grids'][1]['exportTime']['time'] = output_time

    data_in['project']['outputs']['grids'][2]['exportTime']['time'] = output_time

    data_in['project']['outputs']['grids'][3]['exportTime']['time'] = output_time

    data_in['project']['outputs']['grids'][4]['exportTime']['time'] = output_time

    data_in['project']['outputs']['grids'][5]['exportTime']['time'] = output_time

    data_in['project']['outputs']['grids'][5]['startExportTime']['time'] = output_time

    data_in['project']['outputs']['vectors'][0]['perimeterTime']['startTime']['time'] = ignition_start

    data_in['project']['outputs']['vectors'][0]['perimeterTime']['endTime']['time'] = output_time

    data_in['project']['stations']['wxStationData'][0]['streams'][0]['condition']['startTime']['time'] = scenario_start

    replace_in_dict(data_in, 'scen0', scen_name+'_'+ignition_start[0:10])

    with open(job_name, 'w') as f:
        json.dump(data_in, f, indent=2)
    print('fgmj file modified')
# current date for filename
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H:%M")

scen_name_1 = scen_name_1 + "_" + str(formatted_datetime)
scen_name_2 = scen_name_2 + "_" + str(formatted_datetime)
scen_name_3 = scen_name_3 + "_" + str(formatted_datetime)


# edit the job.fgmj files and save them in repective directories
file_name1 = '/testjobs/testjobs/area1/job.fgmj'
file_name2 = '/testjobs/testjobs/area2/job.fgmj'
file_name3 = '/testjobs/testjobs/area3/job.fgmj'
create_job(fgmj_data1,file_name1,scen_name_1,ignition_x_1,ignition_y_1)
create_job(fgmj_data2,file_name2,scen_name_2,ignition_x_2,ignition_y_2)
create_job(fgmj_data3,file_name3,scen_name_3,ignition_x_3,ignition_y_3)

# current working dir
current_directory = os.getcwd()

# get the group id
directory_stat = os.stat(current_directory)

# get group ownership
group_owner_gid = directory_stat.st_gid

parent_directory = os.path.dirname(file_name1)
parent_gid = os.stat(parent_directory).st_gid

# change group ownership
os.chown(file_name1, -1, parent_gid)
os.chown(file_name2, -1, parent_gid)
os.chown(file_name3, -1, parent_gid)


print('modify_fgmj.py done')