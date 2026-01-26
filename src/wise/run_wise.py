import argparse
import json
import numpy as np
import os
import pandas as pd
import subprocess
import xarray as xr
from datetime import datetime
import geopandas as gp
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling, transform_bounds
from affine import Affine

def modify_fgmj(
    scenario_start,
    scenario_end,
    ignition_start,
    ignition_end,
    ignition_y_1,
    ignition_x_1,
    ignition_y_2,
    ignition_x_2,
    ignition_y_3,
    ignition_x_3,
    ignition_y_4,
    ignition_x_4,
    ignition_y_5,
    ignition_x_5,
    ignition_y_6,
    ignition_x_6,
    ignition_y_7,
    ignition_x_7,
    ignition_y_8,
    ignition_x_8,
    ignition_y_9,
    ignition_x_9,
   
):
    
    print("running .fgmj modifier")
    # set scenario names
    scen_name_1 = "scen_fin_kalajoki"
    scen_name_2 = "scen_fin_koli"
    scen_name_3 = "scen_fin_lieksa"
    scen_name_4 = "scen_por_1_norm"
    scen_name_5 = "scen_por_1_break"
    scen_name_6 = "scen_por_2_norm"
    scen_name_7 = "scen_por_2_break"
    scen_name_8 = "scen_por_3_norm"
    scen_name_9 = "scen_por_3_break"

    # set input fgmj path and read the fgmj files
    fgmj_fin_path = "/testjobs/testjobs/job_fin.fgmj"
    fgmj_por_path = "/testjobs/testjobs/job_por.fgmj"

    # Load fgmj files (3 Finland, 6 Portugal)
    fgmj_data_list = []
    for i in range(3):
        with open(fgmj_fin_path, "r") as f:
            fgmj_data_list.append(json.load(f))
    for i in range(6):
        with open(fgmj_por_path, "r") as f:
            fgmj_data_list.append(json.load(f))





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
    def create_job(data_in, job_name, scen_name, ign_lon, ign_lat, weather_path,spat_path):
            
    
        data_in["project"]["scenarios"]["scenarioData"][0]["startTime"]["time"] = (
            scenario_start
        )

        data_in["project"]["scenarios"]["scenarioData"][0]["endTime"]["time"] = (
            scenario_end
        )

        data_in["project"]["scenarios"]["scenarioData"][0]["temporalConditions"][
            "daily"
        ][0]["localStartTime"]["time"] = local_start_time

        data_in["project"]["scenarios"]["scenarioData"][0]["temporalConditions"][
            "daily"
        ][0]["startTime"]["time"] = start_time

        data_in["project"]["scenarios"]["scenarioData"][0]["temporalConditions"][
            "daily"
        ][0]["endTime"]["time"] = end_time

        data_in["project"]["ignitions"]["ignitionData"][0]["startTime"]["time"] = (
            ignition_start
        )

        data_in["project"]["ignitions"]["ignitionData"][0]["ignitions"]["ignitions"][0][
            "polygon"
        ]["polygon"]["points"][0]["x"]["value"] = ign_lon

        data_in["project"]["ignitions"]["ignitionData"][0]["ignitions"]["ignitions"][0][
            "polygon"
        ]["polygon"]["points"][0]["y"]["value"] = ign_lat

        data_in["project"]["outputs"]["grids"][0]["exportTime"]["time"] = output_time

        data_in["project"]["outputs"]["grids"][1]["exportTime"]["time"] = output_time

        data_in["project"]["outputs"]["grids"][2]["exportTime"]["time"] = output_time

        data_in["project"]["outputs"]["grids"][3]["exportTime"]["time"] = output_time

        data_in["project"]["outputs"]["grids"][4]["exportTime"]["time"] = output_time

        data_in["project"]["outputs"]["grids"][5]["exportTime"]["time"] = output_time

        data_in["project"]["outputs"]["grids"][6]["exportTime"]["time"] = output_time

        data_in["project"]["outputs"]["vectors"][0]["perimeterTime"]["startTime"][
            "time"
        ] = ignition_start

        data_in["project"]["outputs"]["vectors"][0]["perimeterTime"]["endTime"][
            "time"
        ] = output_time

        data_in["project"]["stations"]["wxStationData"][0]["streams"][0]["condition"][
            "startTime"
        ]["time"] = scenario_start
        
        
        data_in["project"]["outputs"]["summaries"][0]["filename"] = (
            "/wise_output/scen0/summary.txt"
        )
        
        data_in["project"]["outputs"]["grids"][0]["filename"] = (
            "/wise_output/scen0/max_intensity.tif"
        )
        data_in["project"]["outputs"]["grids"][1]["filename"] = (
            "/wise_output/scen0/max_flame_length.tif"
        )
        data_in["project"]["outputs"]["grids"][2]["filename"] = (
            "/wise_output/scen0/burn_grid.tif"
        )
        data_in["project"]["outputs"]["grids"][3]["filename"] = (
            "/wise_output/scen0/crown_fuel_consumed.tif"
        )
        data_in["project"]["outputs"]["grids"][4]["filename"] = (
            "/wise_output/scen0/surface_fuel_consumed.tif"
        )
        data_in["project"]["outputs"]["grids"][5]["filename"] = (
            "/wise_output/scen0/max_crown_fraction_burned.tif"
        )
        data_in["project"]["outputs"]["grids"][6]["filename"] = (
            "/wise_output/scen0/total_fuel_consumption.tif"
        )
        data_in["project"]["outputs"]["vectors"][0]["filename"] = (
            "/wise_output/scen0/perim.kml"
        )
        
        data_in["project"]["stations"]["wxStationData"][0]["streams"][0]["condition"]["filename"] = (
            weather_path
        )
        
        data_in["project"]["grid"]["fuelMap"]["filename"] = (
            spat_path+"fuel.asc"
        )
        data_in["project"]["grid"]["elevation"]["filename"] = (
            spat_path+"dem.asc"
        )
        data_in["project"]["grid"]["projection"]["filename"] = (
            spat_path+"dem.prj"
        )
               
        replace_in_dict(data_in, "scen0", scen_name + "_" + ignition_start[0:10])

        with open(job_name, "w") as f:
            json.dump(data_in, f, indent=2)
        print("fgmj file modified")

    # current date for filename
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H:%M")

    # List of scenario names
    scen_names = [
        scen_name_1, scen_name_2, scen_name_3,
        scen_name_4, scen_name_5, scen_name_6,
        scen_name_7, scen_name_8, scen_name_9
    ]


    # Corresponding weather paths
    weather_paths = [f"/wise_output/area{i}/Inputs/weather.txt" for i in range(1, 10)]

    # Corresponding spat paths
    spat_paths = [f"/testjobs/testjobs/area{i}/Inputs/" for i in range(1, 10)]

    # Corresponding job filenames
    job_files = [f"/wise_output/area{i}/job.fgmj" for i in range(1, 10)]

    # Corresponding ignition coordinates
    ignition_x = [ignition_x_1, ignition_x_2, ignition_x_3,
                ignition_x_4, ignition_x_5, ignition_x_6,
                ignition_x_7, ignition_x_8, ignition_x_9]

    ignition_y = [ignition_y_1, ignition_y_2, ignition_y_3,
                ignition_y_4, ignition_y_5, ignition_y_6,
                ignition_y_7, ignition_y_8, ignition_y_9]

    # Append formatted datetime to all scenario names
    scen_names = [name + "_" + str(formatted_datetime) for name in scen_names]

    # Create job files
    for i in range(9):
        create_job(
            fgmj_data_list[i],
            job_files[i],
            scen_names[i],
            ignition_x[i],
            ignition_y[i],
            weather_paths[i],
            spat_paths[i]
        )

    # Append ignition start date to scenario names to match the folder names created by WISE
    scen_names = [name + "_" + ignition_start[:10] for name in scen_names]

    # Print done message
    print("modify_fgmj.py done")
    
    return scen_names[0], scen_names[1], scen_names[2], scen_names[3], scen_names[4], scen_names[5], scen_names[6], scen_names[7], scen_names[8] 


def ncdf_edits_multiarea(dataset_path):
    print("running ncdf_edits_multiarea.py")
    # load netcdf dataset
    dataset = xr.open_dataset(dataset_path)

    # calculate wind speed and direction from 10u and 10v components
    wind_speed = np.sqrt(dataset["10u"] ** 2 + dataset["10v"] ** 2)
    dataset["wind_speed"] = wind_speed

    wind_direction_rad = np.arctan2(dataset["10v"], dataset["10u"])
    wind_direction_deg = np.degrees(wind_direction_rad)
    wind_direction_deg = (wind_direction_deg + 360) % 360
    dataset["wind_direction"] = wind_direction_deg

    # calculate relative humidity and convert temperatures to Celsius
    temperature_celsius = dataset["2t"] - 273.15  # Convert from Kelvin to Celsius
    dewpoint_celsius = dataset["2d"] - 273.15  # Convert from Kelvin to Celsius
    relative_humidity = 100 * (
        np.exp((17.625 * dewpoint_celsius) / (243.04 + dewpoint_celsius))
        / np.exp((17.625 * temperature_celsius) / (243.04 + temperature_celsius))
    )

    dataset["relative_humidity"] = relative_humidity
    dataset["temperature"] = temperature_celsius

    # set the ignition coordinates for the nine test areas
    area1_lat = 64.007044
    area1_lon = 24.152986

    area2_lat = 63.050609
    area2_lon = 29.889436

    area3_lat = 63.436092
    area3_lon = 30.541259

    area4_lat = 40.041393
    area4_lon = -8.114061

    area5_lat = 40.041393
    area5_lon = -8.114061

    area6_lat = 40.196173
    area6_lon = -8.137504

    area7_lat = 40.196173
    area7_lon = -8.137504

    area8_lat = 40.125040
    area8_lon = -8.113300

    area9_lat = 40.125040
    area9_lon = -8.113300


    # select only closest cell from netcdf to each ignition location
    area_coords = [
        (area1_lat, area1_lon), (area2_lat, area2_lon), (area3_lat, area3_lon),
        (area4_lat, area4_lon), (area5_lat, area5_lon), (area6_lat, area6_lon),
        (area7_lat, area7_lon), (area8_lat, area8_lon), (area9_lat, area9_lon)
    ]
    
    dataframes = []
    for lat, lon in area_coords:
        nearest_cell = dataset.sel(lat=lat, lon=lon, method="nearest")
        dataframes.append(nearest_cell.to_dataframe())


    # make required dataframe edits
    variables_to_drop = ["10v", "10u", "2t", "2d"]
    for i, df in enumerate(dataframes):
        df.reset_index(inplace=True)
        df.set_index("time", inplace=True)
        df["date"] = df.index.date
        df["hour"] = df.index.time
        dataframes[i] = df.drop(variables_to_drop, axis=1)


    # create datetime series for scenario start and end times (start at each day 10:00 and end same day 21:00)
    combined_datetime_series = pd.to_datetime(dataframes[0].index.date) + pd.to_timedelta(
        [time.hour for time in dataframes[0].index], unit="h"
    )
    combined_datetime_series = pd.Series(combined_datetime_series)

    # reset the index to default integer index
    combined_datetime_series = combined_datetime_series.reset_index(drop=True)

    # select scenario start and end dates
    scenario_start = str(combined_datetime_series.iloc[1])
#    scenario_end = str(combined_datetime_series.iloc[-2])
    scenario_end = str(combined_datetime_series.iloc[-4])
    scenario_start = scenario_start.replace(" ", "T")
    scenario_end = scenario_end.replace(" ", "T")
    scenario_start = scenario_start + ":00"
    scenario_end = scenario_end + ":00"

    dates_at_10 = combined_datetime_series[
        combined_datetime_series.apply(
            lambda x: x.time() == pd.to_datetime("10:00:00").time()
        )
    ]
    dates_at_21 = combined_datetime_series[
        combined_datetime_series.apply(
            lambda x: x.time() == pd.to_datetime("21:00:00").time()
        )
    ]

    # select the last three dates for model run
    dates_at_10 = str(dates_at_10.iloc[0])  # -3 original
    dates_at_10 = dates_at_10.replace(" ", "T")
    dates_at_21 = str(dates_at_21.iloc[-1])
    dates_at_21 = dates_at_21.replace(" ", "T")
    dates_at_10 = dates_at_10 + ":00"
    dates_at_21 = dates_at_21 + ":00"

    # set column order and rename
    new_column_order = ["date", "hour", "temperature", "relative_humidity", "wind_direction", "wind_speed", "tp"]
    column_rename_map = {
        "date": "HOURLY",
        "hour": "HOUR",
        "temperature": "TEMP",
        "relative_humidity": "RH",
        "wind_direction": "WD",
        "wind_speed": "WS",
        "tp": "PRECIP",
    }
    
    for i in range(len(dataframes)):
        dataframes[i].reset_index(inplace=True)
        dataframes[i] = dataframes[i][new_column_order].copy()
        dataframes[i].rename(columns=column_rename_map, inplace=True)
        dataframes[i]["HOURLY"] = pd.to_datetime(dataframes[i]["HOURLY"], format="%d/%m/%Y")
        dataframes[i]["HOUR"] = dataframes[i]["HOUR"].apply(lambda x: x.hour).astype(int)
        dataframes[i] = dataframes[i].round(1)
        dataframes[i]["HOURLY"] = dataframes[i]["HOURLY"].dt.strftime("%d/%m/%Y")

    # save the new .txt format weather files to their designated job folders for WISE runs
    file_path = "/wise_output/"
    
    # Create directories and save weather files
    for i in range(1, 10):
        directory = f"/wise_output/area{i}/Inputs"
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        file_name = f"{file_path}area{i}/Inputs/weather.txt"
        dataframes[i-1].to_csv(file_name, sep=",", index=False)


    # current working dir
    current_directory = os.getcwd()

    # run the modify_fgmj.py script
    print("ncdf_edits_multiarea.py done, starting modify_fgmj.py")
    scen_name_1,scen_name_2,scen_name_3,scen_name_4,scen_name_5,scen_name_6,scen_name_7,scen_name_8,scen_name_9 = modify_fgmj(
        scenario_start,
        scenario_end,
        dates_at_10,
        dates_at_21,
        area1_lat,
        area1_lon,
        area2_lat,
        area2_lon,
        area3_lat,
        area3_lon,
        area4_lat,
        area4_lon,
        area5_lat,
        area5_lon,
        area6_lat,
        area6_lon,
        area7_lat,
        area7_lon,
        area8_lat,
        area8_lon,
        area9_lat,
        area9_lon

    )
    return scen_name_1,scen_name_2,scen_name_3,scen_name_4,scen_name_5,scen_name_6,scen_name_7,scen_name_8,scen_name_9
    
    


def run_wise(
    in_path, out_path, year_start, month_start, day_start, year_end, month_end, day_end
):
    print("running run_wise.py")
    # Provide the data file name for all variables (weekly)
    temp_name = f"{year_start}_{month_start}_{day_start}_T00_to_{year_end}_{month_end}_{day_end}_T23_2t_timestep_60_hourly_mean.nc"  # temperature
    dewpoint_name = f"{year_start}_{month_start}_{day_start}_T00_to_{year_end}_{month_end}_{day_end}_T23_2d_timestep_60_hourly_mean.nc"  # dewpoint temperature
    uwind_name = f"{year_start}_{month_start}_{day_start}_T00_to_{year_end}_{month_end}_{day_end}_T23_10u_timestep_60_hourly_mean.nc"  # u wind
    vwind_name = f"{year_start}_{month_start}_{day_start}_T00_to_{year_end}_{month_end}_{day_end}_T23_10v_timestep_60_hourly_mean.nc"  # v wind
    precip_name = f"{year_start}_{month_start}_{day_start}_T00_00_to_{year_end}_{month_end}_{day_end}_T23_00_avg_tprate_raw_data.nc"  # precipitation

    # read the netcdf files and take variables
    temp_nc = xr.open_dataset(in_path + temp_name)
    dewpoint_nc = xr.open_dataset(in_path + dewpoint_name)
    windu_nc = xr.open_dataset(in_path + uwind_name)
    windv_nc = xr.open_dataset(in_path + vwind_name)
    precip_nc = xr.open_dataset(in_path + precip_name)

    windu_var = windu_nc["10u"]
    windv_var = windv_nc["10v"]
    temp_var = temp_nc["2t"]
    dewpoint_var = dewpoint_nc["2d"]
    precip_var = precip_nc["avg_tprate"] * 3600

    # combine all variables into singular file
    combined_nc = xr.Dataset(
        {
            "10u": windu_var,
            "10v": windv_var,
            "2t": temp_var,
            "2d": dewpoint_var,
            "tp": precip_var,
        }
    )

    file_name = in_path + "combined_ncdf.nc"

    # write the new netcdf file
    combined_nc.to_netcdf(file_name)

    # current working dir
    current_directory = os.getcwd()

    # run the ncdf_edits_multiarea.py script
    scen_name_1, scen_name_2, scen_name_3, scen_name_4, scen_name_5, scen_name_6, scen_name_7, scen_name_8, scen_name_9 = ncdf_edits_multiarea(file_name)

    # run the WISE model for all test areas
    print("launching WISE runs")
    for i in range(1, 10):
        cmd = ["wise", "-r", "4", "-f", "0", "-t", f"/wise_output/area{i}/job.fgmj"]
        subprocess.run(cmd)


    print("WISE runs complete, creating netcdf")
       
    raster_path = "/wise_output/"+scen_name_1+"/burn_grid.tif"
    netcdf_path = f"/wise_output/{year_start}_{month_start}_{day_start}_T00_00_burn_grid.nc"

    # Define raster file names
    raster_names = [
        "burn_grid", "crown_fuel_consumed", "max_crown_fraction_burned",
        "max_flame_length", "max_intensity", "surface_fuel_consumed",
        "total_fuel_consumption"
    ]

    # Base directory
    scen_names = [scen_name_1,scen_name_2,scen_name_3,scen_name_4,scen_name_5,scen_name_6,scen_name_7,scen_name_8,scen_name_9]
    base_path = f"/wise_output/"

    # Loop through each raster file
    for scen_name in scen_names:
        for raster_name in raster_names:
            raster_path = os.path.join(base_path, f"{scen_name}/{raster_name}.tif")
            netcdf_path = os.path.join(base_path, f"{scen_name}/{year_start}_{month_start}_{day_start}_T00_00_{raster_name}.nc")

            # Open the raster file
            with rasterio.open(raster_path) as src:
                # Read the raster data
                raster_data = src.read(1)  # Read the first band
                original_crs = src.crs
                transform = src.transform
                width, height = src.width, src.height

                # Get the bounding box in EPSG:4326 (WGS 84)
                minx, miny, maxx, maxy = transform_bounds(original_crs, "EPSG:4326",
                                                          src.bounds.left, src.bounds.bottom,
                                                          src.bounds.right, src.bounds.top)

                # Generate lat/lon coordinate arrays
                lon = np.linspace(minx, maxx, width)
                lat = np.linspace(maxy, miny, height)  # Flip latitude to maintain correct order

                # Create an xarray dataset
                ds = xr.Dataset(
                    {
                        raster_name: (["lat", "lon"], raster_data),
                    },
                    coords={
                        "lat": lat,
                        "lon": lon,
                    },
                )

                # Add metadata
                ds[raster_name].attrs["units"] = "unknown"
                ds[raster_name].attrs["description"] = f"{raster_name} from Raster"
                ds.attrs["crs"] = "EPSG:4326"

                # Add global attributes from temp_nc to the NetCDF output (if available)
                for attr in ["activity", "dataset", "experiment", "generation", "type", "levtype",
                             "model", "class", "realization", "stream", "resolution", "expver"]:
                    if "temp_nc" in locals() and attr in temp_nc.attrs:
                        ds.attrs[attr] = temp_nc.attrs[attr]

                # Add creation history
                ds.attrs["history"] = "Created on " + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")

                # Save dataset to NetCDF
                ds.to_netcdf(netcdf_path)

                print(f"NetCDF file created: {netcdf_path}")
            
    
    # === Restart File Handling (Only on the 1st of the Month) ===
        if int(day_start) == 1:
            restart_file_path = os.path.join(base_path, f"{year_start}_{month_start}_{day_start}_T00_00_restart_file.nc")
            prev_month = str(int(month_start) - 1).zfill(2)
            prev_year = year_start if month_start != "01" else str(int(year_start) - 1)
            prev_restart_file = os.path.join(base_path, f"{prev_year}_{prev_month}_{day_start}_T00_00_restart_file.nc")

            # Create an empty restart file
            restart_ds = xr.Dataset(attrs={"description": "Restart file for WISE runs"})
            restart_ds.to_netcdf(restart_file_path)
            print(f"Restart file created: {restart_file_path}")

            # Delete the previous restart file if it exists
            if os.path.exists(prev_restart_file):
                os.remove(prev_restart_file)
                print(f"Deleted previous restart file: {prev_restart_file}")


def main():
    # defining file input / output paths
    in_path = "/input_data/"
    
    parser = argparse.ArgumentParser(description="Runscript for data notifier job.")

    parser.add_argument(
        "-year_start", required=True, help="Input year start", default=1
    )
    parser.add_argument(
        "-month_start", required=True, help="Input month start", default=2
    )
    parser.add_argument("-day_start", required=True, help="Input day start", default=3)

    parser.add_argument("-year_end", required=True, help="Input year end", default=4)
    parser.add_argument("-month_end", required=True, help="Input month end", default=5)
    parser.add_argument("-day_end", required=True, help="Input day end", default=6)

    # parser.add_argument('-expid', required=True, help='experiment id', default=7)

    args = parser.parse_args()

    out_path = "/wise_output/"

    run_wise(
        in_path,
        out_path,
        args.year_start,
        args.month_start,
        args.day_start,
        args.year_end,
        args.month_end,
        args.day_end,
    )


if __name__ == "__main__":
    main()




