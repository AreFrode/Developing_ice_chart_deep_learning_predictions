import sys
sys.path.append('/lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/verification_metrics')
sys.path.append('/lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/SimpleUNET')
sys.path.append('/lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/PrepareDataset')
sys.path.append('/lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/ForecastValidation/Forecasts')

import os
import pandas as pd
import glob
import h5py

import numpy as np

from calendar import monthrange
from verification_metrics import IIEE_alt, IIEE_fast, find_ice_edge, ice_edge_length, contourAreaDistribution, minimumDistanceToIceEdge, root_mean_square_error
# from tqdm import tqdm
from helper_functions import read_config_from_csv
from datetime import datetime, timedelta
from netCDF4 import Dataset
from createHDF import remove_open_water_and_fast_ice
from loadClimatologicalIceEdge import load_climatological_ice_edge

# from matplotlib import pyplot as plt

def load_barents(yyyymmdd, lead_time, grid, PATH_TARGET, weights = None):
    # Currently only returns arome member
    PATH_FORECAST = f"/lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/PhysicalModels/Data/{grid}_grid/barents/"
    
    yyyymmdd_datetime = datetime.strptime(yyyymmdd, '%Y%m%d')
    yyyymmdd_valid = (yyyymmdd_datetime + timedelta(days = lead_time - 1)).strftime('%Y%m%d')
    
    yyyymmdd_ml = (yyyymmdd_datetime - timedelta(days = 1)).strftime('%Y%m%d')

    barents_path = glob.glob(f"{PATH_FORECAST}{yyyymmdd[:4]}/{yyyymmdd[4:6]}/barents_mean_b{yyyymmdd}.nc")[0]

    target_path = glob.glob(f"{PATH_TARGET}{yyyymmdd_valid[:4]}/{yyyymmdd_valid[4:6]}/target_v{yyyymmdd_valid}.nc")[0]

    with Dataset(barents_path, 'r') as nc:
        barents_sic = nc.variables['sic'][lead_time - 1, 0, :,:]

    with Dataset(target_path, 'r') as nc:
        target_sic = nc.variables['sic'][:,:]

    return barents_sic, target_sic, yyyymmdd_ml


def load_ml(yyyymmdd, lead_time, grid, PATH_TARGET, weights):
    PATH_FORECAST = f"/lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/PhysicalModels/Data/{grid}_grid/ml/"

    yyyymmdd_datetime = datetime.strptime(yyyymmdd, '%Y%m%d')
    yyyymmdd_valid = (yyyymmdd_datetime + timedelta(days = lead_time)).strftime('%Y%m%d')

    ml_path = glob.glob(f"{PATH_FORECAST}{yyyymmdd[:4]}/{yyyymmdd[4:6]}/{weights}_{yyyymmdd_valid}_b{yyyymmdd}.nc")[0]

    target_path = glob.glob(f"{PATH_TARGET}{yyyymmdd_valid[:4]}/{yyyymmdd_valid[4:6]}/target_v{yyyymmdd_valid}.nc")[0]

    with Dataset(ml_path, 'r') as nc:
        ml_sic = nc.variables['sic'][:,:]

    with Dataset(target_path, 'r') as nc:
        target_sic = nc.variables['sic'][:,:]

    return ml_sic, target_sic, yyyymmdd

def load_nextsim(yyyymmdd, lead_time, grid, PATH_TARGET, weights = None):
    # Currently only returns arome member
    if grid == 'amsr2':
        PATH_FORECAST = f"/lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/PhysicalModels/Data/{grid}_grid/nextsim/"
    
    else:
        PATH_FORECAST = "/lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/PhysicalModels/Data/nextsim/"

    yyyymmdd_datetime = datetime.strptime(yyyymmdd, '%Y%m%d')
    yyyymmdd_valid = (yyyymmdd_datetime + timedelta(days = lead_time - 1)).strftime('%Y%m%d')
    yyyymmdd_ml = (yyyymmdd_datetime - timedelta(days = 1)).strftime('%Y%m%d')

    nextsim_path = glob.glob(f"{PATH_FORECAST}{yyyymmdd[:4]}/{yyyymmdd[4:6]}/nextsim_mean_b{yyyymmdd}.nc")[0]

    target_path = glob.glob(f"{PATH_TARGET}{yyyymmdd_valid[:4]}/{yyyymmdd_valid[4:6]}/target_v{yyyymmdd_valid}.nc")[0]

    with Dataset(nextsim_path, 'r') as nc:
        nextsim_sic = nc.variables['sic'][lead_time - 1, :,:]

    with Dataset(target_path, 'r') as nc:
        target_sic = nc.variables['sic'][:,:]

    return nextsim_sic, target_sic, yyyymmdd_ml

def load_amsr2_trend(yyyymmdd, lead_time, grid, PATH_TARGET, weights = None):
    # Use weights parameter to get osisaf trend
    PATH_FORECAST = f"//lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/PhysicalModels/Data/{grid}_grid/amsr2-trend/"

    yyyymmdd_datetime = datetime.strptime(yyyymmdd, '%Y%m%d')
    yyyymmdd_valid = (yyyymmdd_datetime + timedelta(days = lead_time)).strftime('%Y%m%d')

    amsr2_trend_path = glob.glob(f"{PATH_FORECAST}{yyyymmdd[:4]}/{yyyymmdd[4:6]}/amsr2_trend_b{yyyymmdd}.nc")[0]

    target_path = glob.glob(f"{PATH_TARGET}{yyyymmdd_valid[:4]}/{yyyymmdd_valid[4:6]}/target_v{yyyymmdd_valid}.nc")[0]

    with Dataset(amsr2_trend_path, 'r') as nc:
        amsr2_trend_sic = nc.variables['sic'][lead_time - 1, :,:]

    with Dataset(target_path, 'r') as nc:
        target_sic = nc.variables['sic'][:,:]

    return amsr2_trend_sic, target_sic, yyyymmdd

def load_persistence(yyyymmdd, lead_time, grid, PATH_TARGET, weights = None):
    PATH_FORECAST = f"/lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/PhysicalModels/Data/{grid}_grid/persistence/"

    yyyymmdd_datetime = datetime.strptime(yyyymmdd, '%Y%m%d')
    yyyymmdd_valid = (yyyymmdd_datetime + timedelta(days = lead_time)).strftime('%Y%m%d')

    persistence_path = glob.glob(f"{PATH_FORECAST}{yyyymmdd[:4]}/{yyyymmdd[4:6]}/target_v{yyyymmdd}.nc")[0]

    target_path = glob.glob(f"{PATH_TARGET}{yyyymmdd_valid[:4]}/{yyyymmdd_valid[4:6]}/target_v{yyyymmdd_valid}.nc")[0]

    with Dataset(persistence_path, 'r') as nc:
        persistence_sic = nc.variables['sic'][:,:]

    with Dataset(target_path, 'r') as nc:
        target_sic = nc.variables['sic'][:,:]

    return persistence_sic, target_sic, yyyymmdd

def load_persistence_amsr2(yyyymmdd, lead_time, grid, PATH_TARGET, weights = None):
    PATH_FORECAST = f"/lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/PhysicalModels/Data/amsr2/"

    yyyymmdd_datetime = datetime.strptime(yyyymmdd, '%Y%m%d')
    yyyymmdd_valid = (yyyymmdd_datetime + timedelta(days = lead_time)).strftime('%Y%m%d')

    amsr2_persistence_path = glob.glob(f"{PATH_FORECAST}{yyyymmdd[:4]}/{yyyymmdd[4:6]}/target_v{yyyymmdd}.nc")[0]

    target_path = glob.glob(f"{PATH_TARGET}{yyyymmdd_valid[:4]}/{yyyymmdd_valid[4:6]}/target_v{yyyymmdd_valid}.nc")[0]

    with Dataset(amsr2_persistence_path, 'r') as nc:
        amsr2_persistence_sic = nc.variables['sic'][:,:]

    with Dataset(target_path, 'r') as nc:
        target_sic = nc.variables['sic'][:,:]

    return amsr2_persistence_sic, target_sic, yyyymmdd

def load_osisaf(yyyymmdd, lead_time, grid, PATH_TARGET, weights = None):
    # Use weights parameter to get osisaf trend
    PATH_FORECAST = f"/lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/PhysicalModels/Data/{grid}_grid/osisaf/"

    yyyymmdd_datetime = datetime.strptime(yyyymmdd, '%Y%m%d')
    yyyymmdd_valid = (yyyymmdd_datetime + timedelta(days = lead_time)).strftime('%Y%m%d')

    osisaf_path = glob.glob(f"{PATH_FORECAST}{yyyymmdd[:4]}/{yyyymmdd[4:6]}/osisaf_mean_b{yyyymmdd}.nc")[0]

    target_path = glob.glob(f"{PATH_TARGET}{yyyymmdd_valid[:4]}/{yyyymmdd_valid[4:6]}/target_v{yyyymmdd_valid}.nc")[0]

    with Dataset(osisaf_path, 'r') as nc:
        osisaf_sic = nc.variables['sic'][weights, lead_time - 1, :,:]

    with Dataset(target_path, 'r') as nc:
        target_sic = nc.variables['sic'][:,:]

    return osisaf_sic, target_sic, yyyymmdd

def main():
    product = sys.argv[1]
    lead_time = int(sys.argv[2])
    grid = sys.argv[3]

    try:
        weights = sys.argv[4]

    except IndexError:
        weights = None
    

    if grid == 'nextsim':
        PATH_TARGET = f"/lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/PhysicalModels/Data/targets/"
        side_length = 3

    elif grid == 'amsr2':
        PATH_TARGET = f"/lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/PhysicalModels/Data/amsr2/"
        side_length = 6.25

    else:
        exit('No valid target grid supplied')

    load_func = None

    if product == 'barents':
        load_func = load_barents

    elif product == 'ml':
        load_func = load_ml
        product = weights
        # assert len(sys.argv) > 3, "To compute ml stats, supply valid model string"
        # path_config = "/lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/SimpleUNET/TwoDayForecast/outputs/"
        # weights = "weights_05011118"
        # config = read_config_from_csv(f"{path_config}configs/{weights}.csv")
        # osisaf_trend = config['osisaf_trend']

    elif product == 'nextsim':
        # PATH_FORECAST = f"/lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/PhysicalModels/Data/nextsim/"
        load_func = load_nextsim

    elif product == 'osisaf':
        # assert len(sys.argv) > 3, "To compute osisaf stats, supply osisaf trend length"
        # PATH_FORECAST = f"/lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/PhysicalModels/Data/osisaf/osisaf_trend_{osisaf_trend}/"
        load_func = load_osisaf

        # OsiSaf 5-day trend
        weights = 2

    elif product == 'persistence':
        load_func = load_persistence
    
    elif product == 'amsr2_persistence':
        load_func = load_persistence_amsr2

    elif product == 'amsr2_trend':
        load_func = load_amsr2_trend

    elif product == 'ice_chart':
        load_func = load_ice_charts

    else:
        print("No valid product supplied")
        exit()


    PATH_OUTPUTS = f"/lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/PhysicalModels/Data/{grid}_grid/lead_time_{lead_time}/"

    PATH_COMMONS = f"/lustre/storeB/users/arefk/MScThesis_AreKvanum2022_SeaIceML/PhysicalModels/Data/{grid}_commons.nc"
    
    # if product == 'ml' or product == 'osisaf':
    #     PATH_OUTPUTS += f"osisaf_trend_{osisaf_trend}/"

    if not os.path.exists(PATH_OUTPUTS):
        os.makedirs(PATH_OUTPUTS)

    output_list = []

    with Dataset(PATH_COMMONS, 'r') as nc:
        lat = nc.variables['lat'][:,:]
        lon = nc.variables['lon'][:,:]
        lsmask = nc.variables['lsmask'][:,:]

    year = 2022
    months = []
    days = []
    for month in range(1, 13):
        months.append(month)
        days.append(monthrange(int(year), (month))[1])

    # Updated for compatibility wiht IceChartLength
    conc = '10-40%'
    # conc = '15%'
    climatological_ice_edge = load_climatological_ice_edge(2022, conc, lead_time, product = grid)
    # climatological_ice_edge = load_climatological_ice_edge(2022, conc, lead_time)
 
    for i, month in enumerate(months):
        for dd in range(1, days[i] + 1):
        # for dd in range(1, 4):
            # Load time of target
            # Assume forecast initiated lead_time - 1 day before target valid
            yyyymmdd = f"{year}{month:02d}{dd:02d}"
            print(yyyymmdd)

            try:
                sic_forecast, sic_target, yyyymmdd_ml = load_func(yyyymmdd, lead_time, grid, PATH_TARGET, weights)
                climatological_ice_edge[conc].loc[yyyymmdd_ml]

            except (IndexError, KeyError):
                continue

            # sic_target = remove_open_water_and_fast_ice(sic_target)

            # ice_edge_target = find_ice_edge(sic_target, lsmask)
            # target_length = ice_edge_length(ice_edge_target, s = side_length)

            # ice_edge_forecast = find_ice_edge(sic_forecast, lsmask)
            # forecast_length = ice_edge_length(ice_edge_forecast, s = side_length)

            rmse = root_mean_square_error(sic_forecast, sic_target, lsmask)

            NIIEE = []
            for i in range(1, 7):
                niiee = IIEE_alt(sic_forecast, sic_target, lsmask, side_length = side_length, threshold = i)
                NIIEE.append((niiee[0].sum() + niiee[1].sum()) / climatological_ice_edge[conc].loc[yyyymmdd_ml]) # 04.10.23 Changed to yyyymmdd_ml here, should be correct

            area_dist_target = contourAreaDistribution(sic_target, lsmask, num_classes = 7, side_length = side_length)
            area_dist_forecast = contourAreaDistribution(sic_forecast, lsmask, num_classes = 7, side_length = side_length)

            sic_forecast = np.where(sic_forecast == 1, 0, sic_forecast)

            niiee_no_1contour = IIEE_alt(sic_forecast, sic_target, lsmask, side_length = side_length, threshold = 1)

            # a_plus_minimum_distance = minimumDistanceToIceEdge(a_plus, ice_edge_target, lat, lon)
            # a_minus_minimum_distance = minimumDistanceToIceEdge(a_minus, ice_edge_target, lat, lon)

            # output_list.append([pd.to_datetime(yyyymmdd_ml, format="%Y%m%d"), target_length, forecast_length, np.mean([target_length, forecast_length]), a_plus.sum() + a_minus.sum(), a_plus.sum(), a_minus.sum(), a_plus_minimum_distance.mean(), a_minus_minimum_distance.mean()] + area_dist_target.tolist() + area_dist_forecast.tolist())
            output_list.append([pd.to_datetime(yyyymmdd_ml, format="%Y%m%d"), rmse, *NIIEE, *area_dist_forecast.tolist(), *area_dist_target.tolist(), (niiee_no_1contour[0].sum() + niiee_no_1contour[1].sum()) / climatological_ice_edge[conc].loc[yyyymmdd_ml]])


    # output_df = pd.DataFrame(output_list, columns = ['date', 'target_length', 'forecast_length', 'mean_length', 'IIEE', 'a_plus', 'a_minus', 'mean_minimum_distance_to_ice_edge_a_plus', 'mean_minimum_distance_to_ice_edge_a_minus', 'target_area0', 'target_area1', 'target_area2', 'target_area3', 'target_area4', 'target_area5', 'target_area6', 'forecast_area0', 'forecast_area1', 'forecast_area2', 'forecast_area3', 'forecast_area4', 'forecast_area5', 'forecast_area6'])
    output_df = pd.DataFrame(output_list, columns = ['date', 'rmse', *[f"NIIEE_{i}" for i in range(1, 7)], *[f"forecast_area{i}" for i in range(7)], *[f"target_area{i}" for i in range(7)], 'niiee_no_1contour'])

    output_df = output_df.set_index('date')
    output_df.to_csv(f"{PATH_OUTPUTS}{product}.csv")
    


if __name__ == "__main__":
    main()
