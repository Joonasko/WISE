import netCDF4 as nc
import numpy as np
import datetime as dt

def generate_example_netcdf(output_file):
        # Create time values for 48 hours, every hour
        start_time = dt.datetime(2021, 6, 25, 0, 0)
        time_values = [start_time + dt.timedelta(hours=i) for i in range(168)]

        # Create latitude and longitude values for 5 points
        lat_values = np.linspace(64.0, 64.2, 5)
        lon_values = np.linspace(24.0, 24.2, 5)

        # Create temperature, relative humidity, wind speed, wind direction, and precipitation data
        temperature_data = np.random.uniform(25, 35, size=(168, 5, 5))
        relhum_data = np.random.uniform(20, 50, size=(168, 5, 5))
        ws_data = np.random.uniform(4, 12, size=(168, 5, 5))
        wd_data = np.random.uniform(0, 360, size=(168, 5, 5))
        precip_data = np.random.uniform(0, .2, size=(168, 5, 5))

        # Create the NetCDF file
        with nc.Dataset(output_file, 'w') as dataset:
            # Define dimensions
            time_dim = dataset.createDimension('time', len(time_values))
            point_dim = dataset.createDimension('point', len(lat_values))

            # Create variables
            time_var = dataset.createVariable('time', 'i4', ('time',))
            lat_var = dataset.createVariable('latitude', 'f4', ('point',))
            lon_var = dataset.createVariable('longitude', 'f4', ('point',))
            temp_var = dataset.createVariable('temperature', 'f4', ('time', 'point', 'point'))
            relhum_var = dataset.createVariable('relative_humidity', 'f4', ('time', 'point', 'point'))
            ws_var = dataset.createVariable('wind_speed', 'f4', ('time', 'point', 'point'))
            wd_var = dataset.createVariable('wind_direction', 'f4', ('time', 'point', 'point'))
            precip_var = dataset.createVariable('precipitation', 'f4', ('time', 'point', 'point'))

            # Set variable attributes
            time_var.units = 'hours since 2023-07-25 00:00:00'
            lat_var.units = 'degrees_north'
            lon_var.units = 'degrees_east'
            temp_var.units = 'Celsius'
            relhum_var.units = 'percent'
            ws_var.units = 'm/s'
            wd_var.units = 'degrees'
            precip_var.units = 'mm'

            # Write data to variables
            time_var[:] = nc.date2num(time_values, units=time_var.units)
            lat_var[:] = lat_values
            lon_var[:] = lon_values
            temp_var[:] = temperature_data
            relhum_var[:] = relhum_data
            ws_var[:] = ws_data
            wd_var[:] = wd_data
            precip_var[:] = precip_data

if __name__ == "__main__":
    output_file = "example_weather_data.nc"
    generate_example_netcdf(output_file)
    print(f"Example NetCDF file '{output_file}' generated.")
