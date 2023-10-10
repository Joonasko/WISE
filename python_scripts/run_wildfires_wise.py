print("Starting run!")

import os
import xarray
import subprocess
#import gsv

print("Running source load modules lumi")
command = "source /scratch/project_465000454/kolstela/a0c1/workflow/gsv_interface/load_modules_lumi.sh"
completed_lumi_modules = subprocess.run(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True)

print("Standard Error:")
print(completed_lumi_modules.stderr)

print(completed_lumi_modules.returncode)

from gsv import GSVRetriever

print("GSVRetriever imported")


gsv = GSVRetriever()
request = {
          "domain": "g",
          "class": "rd",
          "expver": "hz9n",
          "stream": "lwda",
          "type": "fc",
          "anoffset": 9,
          "date": "20200120",
          "time": "0000",
          "param": ["10u", "10v", "2t"],
          "levtype": "sfc",
          "step": "0/to/24/by/6",
          "grid": "1.0/1.0",
          "method": "nn"
          }
testi = gsv.request_data(request)






expid = "a0c1"
dirout = f"/scratch/project_465000454/tmp/{expid}/"
f = open(f"{dirout}/myfile.txt", "w")

subprocess.call(["python3","/projappl/project_465000454/kolstela/wise_lumi2/testrun.py"])

script_path = "/projappl/project_465000454/kolstela/wise_lumi2/full_run.sh"
command = ["sh", script_path]

completed_process = subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True)

print("Standard Error:")
print(completed_process.stderr)

print(completed_process.returncode)


print("Run complete")
