print('running .fgmj modifier')

import os
import sys
import json

start_time = sys.argv[1]
end_time = sys.argv[2]
ignition_x_1 = float(sys.argv[3])
ignition_y_1 = float(sys.argv[4])
ignition_x_2 = float(sys.argv[5])
ignition_y_2 = float(sys.argv[6])
ignition_x_3 = float(sys.argv[7])
ignition_y_3 = float(sys.argv[8])
scen_name_1 = 'scen_kalajoki'
scen_name_2 = 'scen_koli'
scen_name_3 = 'scen_lohja'

#print(start_time)
#print(end_time)

#with open('/mnt/d/wise/wise_area_data/area1/input.txt', 'r') as f:
#    lines = f.readlines()

#fgmj_dir = lines[0].strip()
#fgmj1_path = '/mnt/d/wise/wise_area_data/area1/job.fgmj'
#fgmj2_path = '/mnt/d/wise/wise_area_data/area2/job.fgmj'
#fgmj3_path = '/mnt/d/wise/wise_area_data/area3/job.fgmj'

fgmj1_path = '/projappl/project_465000454/kolstela/wise_lumi/testjobs/area1/job.fgmj'
fgmj2_path = '/projappl/project_465000454/kolstela/wise_lumi/testjobs/area2/job.fgmj'
fgmj3_path = '/projappl/project_465000454/kolstela/wise_lumi/testjobs/area3/job.fgmj'

#filename = 'job.fgmj'
#fgmj_dir = '/testjobs/job/'

#fgmj_dir = os.path.join(fgmj_dir,filename)
#print(fgmj_dir)

with open(fgmj1_path, 'r') as f:
    data1 = json.load(f)

with open(fgmj2_path, 'r') as f:
    data2 = json.load(f)

with open(fgmj3_path, 'r') as f:
    data3 = json.load(f)

#scenario_start = lines[1].strip()
#scenario_end = lines[2].strip()
#local_start_time = lines[3].strip()
#start_time = lines[4].strip()
#end_time = lines[5].strip()
#ignition_start = lines[6].strip()
#output_time = scenario_end
#ignition_x = float(lines[7].strip())
#ignition_y = float(lines[8].strip())

scenario_start = start_time
scenario_end = end_time
local_start_time = start_time
start_time = start_time
end_time = end_time
ignition_start = start_time
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


def create_job(data, job_name, scen_name, ign_lat, ign_lon):

    data['project']['scenarios']['scenarioData'][0]['startTime']['time'] = scenario_start

    data['project']['scenarios']['scenarioData'][0]['endTime']['time'] = scenario_end

    data['project']['scenarios']['scenarioData'][0]['temporalConditions']['daily'][0]['localStartTime']['time'] = local_start_time

    data['project']['scenarios']['scenarioData'][0]['temporalConditions']['daily'][0]['startTime']['time'] = start_time

    data['project']['scenarios']['scenarioData'][0]['temporalConditions']['daily'][0]['endTime']['time'] = end_time

    data['project']['ignitions']['ignitionData'][0]['startTime']['time'] = ignition_start

    data['project']['ignitions']['ignitionData'][0]['ignitions']['ignitions'][0]['polygon']['polygon']['points'][0]['x']['value'] = ign_lat

    data['project']['ignitions']['ignitionData'][0]['ignitions']['ignitions'][0]['polygon']['polygon']['points'][0]['y']['value'] = ign_lon

    data['project']['outputs']['grids'][0]['exportTime']['time'] = output_time

    data['project']['outputs']['grids'][1]['exportTime']['time'] = output_time

    data['project']['outputs']['grids'][2]['exportTime']['time'] = output_time

    data['project']['outputs']['grids'][2]['startExportTime']['time'] = output_time

    replace_in_dict(data, 'scen0', scen_name)

    with open(job_name, 'w') as f:
        json.dump(data, f, indent=2)
    print('fgmj file modified')

#create_job(data1,'/mnt/d/wise/wise_area_data/testjobs/area1/job.fgmj',scen_name_1,ignition_y_1,ignition_x_1)
#create_job(data2,'/mnt/d/wise/wise_area_data/testjobs/area2/job.fgmj',scen_name_2,ignition_y_2,ignition_x_2)
#create_job(data3,'/mnt/d/wise/wise_area_data/testjobs/area3/job.fgmj',scen_name_3,ignition_y_3,ignition_x_3)

create_job(data1,'/projappl/project_465000454/kolstela/wise_lumi/testjobs/area1/job.fgmj',scen_name_1,ignition_y_1,ignition_x_1)
create_job(data2,'/projappl/project_465000454/kolstela/wise_lumi/testjobs/area2/job.fgmj',scen_name_2,ignition_y_2,ignition_x_2)
create_job(data3,'/projappl/project_465000454/kolstela/wise_lumi/testjobs/area3/job.fgmj',scen_name_3,ignition_y_3,ignition_x_3)

print('modify_fgmj.py done')