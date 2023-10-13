#!/usr/bin/python3
print('running .fgmj modifier')

import os
import sys
import json

#print("sys argv 7")
#print(sys.argv[7])
#print("sys argv 8")
#print(sys.argv[8])
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

scen_name_1 = 'scen_kalajoki'
scen_name_2 = 'scen_koli'
scen_name_3 = 'scen_lieksa'

#print(start_time)
#print(end_time)

#with open('/mnt/d/wise/wise_area_data/area1/input.txt', 'r') as f:
#    lines = f.readlines()

#fgmj_dir = lines[0].strip()
#fgmj_path = '/mnt/d/wise/wise_lumi/wise_lumi/testjobs/job.fgmj'
fgmj_path = '/testjobs/testjobs/job.fgmj'

#fgmj1_path = '/projappl/project_465000454/kolstela/wise_lumi/testjobs/area1/job.fgmj'
#fgmj2_path = '/projappl/project_465000454/kolstela/wise_lumi/testjobs/area2/job.fgmj'
#fgmj3_path = '/projappl/project_465000454/kolstela/wise_lumi/testjobs/area3/job.fgmj'

#filename = 'job.fgmj'
#fgmj_dir = '/testjobs/job/'

#fgmj_dir = os.path.join(fgmj_dir,filename)
#print(fgmj_dir)

with open(fgmj_path, 'r') as f:
    fgmj_data1 = json.load(f)

with open(fgmj_path, 'r') as f:
    fgmj_data2 = json.load(f)

with open(fgmj_path, 'r') as f:
    fgmj_data3 = json.load(f)

#scenario_start = lines[1].strip()
#scenario_end = lines[2].strip()
#local_start_time = lines[3].strip()
#start_time = lines[4].strip()
#end_time = lines[5].strip()
#ignition_start = lines[6].strip()
#output_time = scenario_end
#ignition_x = float(lines[7].strip())
#ignition_y = float(lines[8].strip())

scenario_start = ignition_start
scenario_end = scenario_end
local_start_time = ignition_start
start_time = ignition_start
end_time = scenario_end
ignition_start = ignition_start
output_time = scenario_end


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

    data_in['project']['outputs']['grids'][2]['startExportTime']['time'] = output_time

    data_in['project']['outputs']['grids'][2]['startExportTime']['time'] = output_time

    data_in['project']['outputs']['vectors'][0]['perimeterTime']['startTime']['time'] = ignition_start

    data_in['project']['outputs']['vectors'][0]['perimeterTime']['endTime']['time'] = output_time

    data_in['project']['stations']['wxStationData'][0]['streams'][0]['condition']['startTime']['time'] = scenario_start

    replace_in_dict(data_in, 'scen0', scen_name+'_'+ignition_start[0:10])

    with open(job_name, 'w') as f:
        json.dump(data_in, f, indent=2)
    print('fgmj file modified')

#create_job(fgmj_data1,'/mnt/d/wise/wise_lumi/wise_lumi/testjobs/area1/job.fgmj',scen_name_1,ignition_x_1,ignition_y_1)
#create_job(fgmj_data2,'/mnt/d/wise/wise_lumi/wise_lumi/testjobs/area2/job.fgmj',scen_name_2,ignition_x_2,ignition_y_2)
#create_job(fgmj_data3,'/mnt/d/wise/wise_lumi/wise_lumi/testjobs/area3/job.fgmj',scen_name_3,ignition_x_3,ignition_y_3)

create_job(fgmj_data1,'/testjobs/testjobs/area1/job.fgmj',scen_name_1,ignition_x_1,ignition_y_1)
create_job(fgmj_data2,'/testjobs/testjobs/area2/job.fgmj',scen_name_2,ignition_x_2,ignition_y_2)
create_job(fgmj_data3,'/testjobs/testjobs/area3/job.fgmj',scen_name_3,ignition_x_3,ignition_y_3)

print('modify_fgmj.py done')