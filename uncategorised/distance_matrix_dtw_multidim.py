import copy

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
from tslearn.metrics import dtw
from tslearn.clustering import TimeSeriesKMeans, silhouette_score
from tslearn.utils import to_time_series_dataset

warnings.filterwarnings('ignore')
import pickle
# from dtw import dtw, symmetric2
import os


def pickle_object(o, filepath):
    with open(filepath, 'wb') as f:
        pickle.dump(o, f)


def temp_plotter(data):
    plt.plot(data)
    plt.savefig("./intermediate_files/temp.png")
    plt.close()


def get_diffed_laps(all_laps, diff_col='Position_cm'):
    for lap_index in range(len(all_laps)):
        all_laps[lap_index][diff_col] = all_laps[lap_index][diff_col].diff()  # .diff()
        all_laps[lap_index] = all_laps[lap_index].dropna()
    return all_laps


def get_lap_list_from_mouse_dict(mouse_data: dict) -> list:
    """

    :param mouse_data:
    :return:
    """
    all_mice_data = []
    for mouse in mouse_data:
        for item in mouse_data[mouse]:
            item.insert(column='mouse_id', value=mouse, loc=0)
            all_mice_data.append(item)
    return all_mice_data


config = configparser.ConfigParser()
config.read('/home/mvishnu/projects/decode/config')
non_artefact_lap_info = pd.read_csv("/home/mvishnu/Documents/work/DECODE/data/trials_insignificant_artifacts.csv")
day0_6_data = dl.Day0to6_Loader(config, non_artefact_lap_info[non_artefact_lap_info.day.isin(['day1', 'day5'])])

# all_data_unsplit, unsplit_metadata = day0_6_data.get_all_behavioural_data_dict(split_laps=False)
all_data_split, split_metadata = day0_6_data.get_all_behavioural_data_dict(split_laps=True)

all_laps = get_lap_list_from_mouse_dict(all_data_split)
all_laps_diff = get_diffed_laps(copy.deepcopy(all_laps), diff_col='Position_cm')


def pairwise_dtw_distance(ts1, ts2):
    return dtw(ts1, ts2)


def dm(lap_list, x_cols=['Position_cm', 'Licks'], step_pattern="symmetric2", window_type='slantedband',
       window_args={'window_size': 50}):
    d_mx = np.zeros(len(lap_list) ** 2).reshape(len(lap_list), -1)
    for i in tqdm(range(len(lap_list))):
        for j in range(i + 1, len(lap_list)):
            try:
                d_mx[i][j] = dtw(lap_list[i][x_cols], lap_list[j][x_cols])  # , step_pattern=step_pattern,
                # window_type=window_type, window_args=window_args, distance_only=True).distance
            except:
                d_mx[i][j] = np.inf
            try:
                d_mx[j][i] = dtw(lap_list[j][x_cols], lap_list[i][x_cols])  # , step_pattern=step_pattern,
                # window_type='slantedband', window_args=window_args, distance_only=True).distance
            except:
                d_mx[j][i] = np.inf
    return d_mx


diffed_dtw = dm(all_laps_diff, x_cols=['Position_cm'])
pickle_object(diffed_dtw, os.path.join(os.getcwd(), 'diffed_dtw.pkl'))
print("Diffed DTW complete")

undiffed_dtw = dm(all_laps, x_cols=['Position_cm', 'Velocity', 'Licks', 'Piezo'])
pickle_object(diffed_dtw, os.path.join(os.getcwd(), 'undiffed_dtw.pkl'))

import numpy as np
