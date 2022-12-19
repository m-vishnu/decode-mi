import pandas as pd
import os
from matplotlib import pyplot as plt
import configparser
import data.loaders as dl
import warnings
from tqdm import tqdm
import numpy as np
import stumpy
import tslearn
from tslearn.clustering import TimeSeriesKMeans, silhouette_score
from tslearn.utils import to_time_series_dataset

warnings.filterwarnings('ignore')
import pickle
from dtw import *


def temp_plotter(data):
    plt.plot(data)
    plt.savefig("./intermediate_files/temp.png")
    plt.close()


def get_diffed_laps(all_laps, diff_col='Position_cm'):
    for lap_index in range(len(all_laps)):
        all_laps[lap_index]['Position_cm'] = all_laps[lap_index]['Position_cm'].diff().diff()
        all_laps[lap_index] = all_laps[lap_index].dropna()
    return all_laps


def get_lap_list_from_mouse_dict(mouse_data: list):
    """

    :param mouse_data:
    :return:
    """
    all_mice_data = []
    for mouse in mouse_data[0]:
        all_mice_data.extend(mouse_data[0][mouse])
    return all_mice_data


config = configparser.ConfigParser()
config.read('/home/mvishnu/projects/decode/config')
day0_6_data = dl.Day0to6_Loader(config)

all_data_unsplit = day0_6_data.get_all_behavioural_data_dict(split_laps=False)
all_data_split = day0_6_data.get_all_behavioural_data_dict(split_laps=True)

all_laps = get_lap_list_from_mouse_dict(all_data_split)
all_laps_diff = get_diffed_laps(all_laps.copy(), diff_col='Position_cm')


def dm(lap_list, x_cols=['Position_cm', 'Licks'], step_pattern="symmetric2", window_type = 'slantedband', window_args = {'window_size': 50}):
    d_mx = np.zeros(len(lap_list) ** 2).reshape(len(lap_list), -1)
    for i in range(len(lap_list)):
        for j in range(i+1, len(lap_list)):
            try:
                d_mx[i][j] = dtw(lap_list[i][x_cols], lap_list[j][x_cols], step_pattern=step_pattern,
                                 window_type=window_type, window_args=window_args, distance_only=True).distance
            except:
                d_mx[i][j] = np.inf
            try:
                d_mx[j][i] = dtw(lap_list[j][x_cols], lap_list[i][x_cols], step_pattern=step_pattern,
                                 window_type='slantedband', window_args=window_args, distance_only=True).distance
            except:
                d_mx[j][i] = np.inf
    return d_mx

diffed_dwt = dm(all_laps_diff, x_cols=['Position_cm'])
undiffed_dwt = dm(all_laps, x_cols=['Position_cm'])