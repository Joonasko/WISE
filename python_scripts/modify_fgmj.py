#print("running .fgmj modifier")

import sys
import json

with open("/python_scripts/input.txt", "r") as f:
    lines = f.readlines()

fgmj_dir = lines[0].strip()
fgmj_dir = "/testjobs/job/"

with open(fgmj_dir + "job.fgmj", "r") as f:
    data = json.load(f)

scenario_start = lines[1].strip()
scenario_end = lines[2].strip()
local_start_time = lines[3].strip()
start_time = lines[4].strip()
end_time = lines[5].strip()
ignition_start = lines[6].strip()
output_time = scenario_end


data['project']['scenarios']['scenarioData'][0]['startTime']['time'] = scenario_start

data['project']['scenarios']['scenarioData'][0]['endTime']['time'] = scenario_end

data['project']['scenarios']['scenarioData'][0]['temporalConditions']['daily'][0]['localStartTime']['time'] = local_start_time

data['project']['scenarios']['scenarioData'][0]['temporalConditions']['daily'][0]['startTime']['time'] = start_time

data['project']['scenarios']['scenarioData'][0]['temporalConditions']['daily'][0]['endTime']['time'] = end_time

data['project']['ignitions']['ignitionData'][0]['startTime']['time'] = ignition_start

data['project']['outputs']['grids'][0]['exportTime']['time'] = output_time

data['project']['outputs']['grids'][1]['exportTime']['time'] = output_time

data['project']['outputs']['grids'][2]['exportTime']['time'] = output_time

data['project']['outputs']['grids'][2]['startExportTime']['time'] = output_time


with open(fgmj_dir + 'job.fgmj', 'w') as f:
    json.dump(data, f, indent=2)
print("fgmj file modified")
