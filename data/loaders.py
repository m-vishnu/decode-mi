import pandas as pd
import numpy as np
import h5py
import os


def get_mouse_files_data_frame(root_folder="/home/mvishnu/Documents/work/DECODE/data/Day0to6/",
                               replace_str="/home/mvishnu/Documents/work/DECODE/data/Day0to6/"):
    fileinfo = []  # pd.DataFrame(columns=["Mouse_ID","Type","Group", "Day", "Filename"])
    for path, subdirs, files in os.walk(root_folder):
        for file in files:
            if file.find(".h5") > 0:
                file_path = path + "/" + file
                path = path.replace(replace_str, "")
                m_type, day, group, mouse_id = path.split("/")
                fileinfo.append([mouse_id, m_type, group, day, file_path])
    mouse_data = pd.DataFrame(fileinfo, columns=["Mouse_ID", "Type", "Group", "Day", "Filename"])
    return mouse_data


def load_h5py_file(filepath):
    return pd.read_hdf(filepath)

def split_mouse_runs(df: pd.DataFrame):
    dfs = []
    prev_lap = 0
    for i in range(1,len(df)):
        if df.iloc[i]["Position_cm"] - df.iloc[i-1]["Position_cm"] < - 100:
            dfs.append(df.iloc[prev_lap:i])
    return dfs

mouse_data = get_mouse_files_data_frame()
mouse_data.iloc[0]['Mouse_ID']
mouse_data_x = mouse_data[mouse_data['Mouse_ID']=='95']

sample_mouse_data = load_h5py_file(mouse_data.iloc[0]['Filename'])
sample_mouse_split = split_mouse_runs(sample_mouse_data)

import seaborn as sns
sns.lineplot(data=sample_mouse_split[0],x='Position_cm', y='Licks')