import pandas as pd
import numpy as np
import h5py
import os


def get_mouse_files_data_frame(root_folder, replace_str):
    """
    Given the root folder, it explores all subdirectories and gives a data frame with the metadata for each mouse, and
    the filepath to its data.
    :param root_folder: The root folder of the file path. See config file for details.
    :param replace_str: Just a way to make the resulting pandas data frame a bit prettier. Replaces the path prefix to
    the root directory that contains all the data files within subfolders.
    :return: DataFrame with the metadata (incl. filepaths) to all mice.
    """
    fileinfo = []
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
    """
    Reads the h5py file with the behavioural data
    :param filepath: Path to file
    :return: DataFrame with the behavioural data
    """
    return pd.read_hdf(filepath)


def split_mouse_runs(df: pd.DataFrame):
    """
    Takes the behavioural data, and splits into an array of DataFrames. Each item in the list is one run of the
    treadmill (0-360cm)
    :param df: DataFrame with the behavioural data. Assumed that the position column changing by more than 100cm in one
    time step signifies a new "lap".
    :return: list of DataFrame objects, one per lap.
    """
    dfs = []
    prev_lap = 0
    for i in range(1, len(df)):
        if df.iloc[i]["Position_cm"] - df.iloc[i - 1]["Position_cm"] < - 100:
            dfs.append(df.iloc[prev_lap:i])
            prev_lap = i
    return dfs


if "__name__" == "__main__":
    print("this file is not meant to be run. Please use the functions in your own scripts instead.")
