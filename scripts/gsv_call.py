from gsv import GSVRetriever


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
  "param": ["10u", "10v", "2t", "2d", "tp"],
  "levtype": "sfc",
  "step": "0/to/160/by/1",
  "grid": "1.0/1.0",
  "method": "nn",
  "area": "72/15/58/40"
}
test_dataset = gsv.request_data(request)
output_file = "/scratch/project_465000454/kolstela/output_dataset_week.nc"
test_dataset.to_netcdf(output_file)