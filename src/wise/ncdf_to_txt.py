import netCDF4 as nc
import numpy as np
import sys

lat_index = 0
lon_index = 0


def create_txt_file(input_file, output_file):
    # Open the NetCDF file
    with nc.Dataset(input_file, 'r') as dataset:
        # Get variable data
        time_var = dataset.variables['time']
        lat_var = dataset.variables['latitude']
        lon_var = dataset.variables['longitude']
        temp_var = dataset.variables['temperature']
        relhum_var = dataset.variables['relative_humidity']
        ws_var = dataset.variables['wind_speed']
        wd_var = dataset.variables['wind_direction']
        precip_var = dataset.variables['precipitation']

        # Get data values
        time_values = nc.num2date(time_var[:], units=time_var.units)
        lat_values = lat_var[:]
        lon_values = lon_var[:]
        temp_data = temp_var[:,lat_index,lon_index]
        relhum_data = relhum_var[:,lat_index,lon_index]
        ws_data = ws_var[:,lat_index,lon_index]
        wd_data = wd_var[:,lat_index,lon_index]
        precip_data = precip_var[:,lat_index,lon_index]

    # Create the .txt file
    with open(output_file, 'w') as txt_file:
        # Write header row
        txt_file.write("HOURLY,HOUR,TEMP,RH,WD,WS,PRECIP\n")

        # Write data rows
        for i in range(len(time_values)):
            hourly_time = time_values[i].strftime("%d/%m/%Y")
            hour = time_values[i].hour
            txt_file.write(f"{hourly_time},{hour},{temp_data[i]:.1f},{relhum_data[i]:.1f},{wd_data[i]:.1f},{ws_data[i]:.1f},{precip_data[i]:.1f}\n")


if __name__ == "__main__":
    #if len(sys.argv) != 2:
    #  print("Usage: python3 ncdf_to_txt.py <output_file>")
    #  sys.exit(1)
    input_file = "example_weather_data.nc"
    #output_file = sys.argv[1]
    output_file = "/testjobs/job/Inputs/weather.txt"
    create_txt_file(input_file, output_file)
    print(f"Example .txt file '{output_file}' generated.")
