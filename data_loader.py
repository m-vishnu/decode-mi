# Author: Vishnu Unnikrishnan
import pandas as pd

# This is a sample Python script.
from data import loaders
import configparser
import pickle


def load_behavioural_data_as_dict(mouse_metadata: pd.DataFrame, split_laps: bool):
    if split_laps:
        return {x[0]: loaders.split_mouse_runs(loaders.load_h5py_file(x[1])) for x in
                mouse_metadata[['Mouse_ID', 'Filename']].values}
    else:
        return {x[0]: loaders.load_h5py_file(x[1]) for x in mouse_metadata[['Mouse_ID', 'Filename']].values}


def pickle_data(obj_to_pickle, file_path: str):
    with open(file_path, 'w') as pickle_file:
        pickle.dump(obj_to_pickle, pickle_file)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config')

    mouse_data = loaders.get_mouse_files_data_frame(root_folder=config['DEFAULT']['data_root'],
                                                    replace_str=config['DEFAULT']['replace_path_str'])

    # If you want separate data frames for each 'lap' that the mouse ran in its trial, ie, 1 time series per lap per mouse.
    if config['DEFAULT']['split_mouse_laps'].strip().lower() == 'true':
        all_behaviroual_data = load_behavioural_data_as_dict(mouse_metadata=mouse_data, split_laps=True)

    # If you want to load the full data from the mouse as a single long time series that contains multiple laps.
    elif config['DEFAULT']['split_mouse_laps'].strip().lower() == 'false':
        all_behavioural_data = load_behavioural_data_as_dict(mouse_metadata=mouse_data, split_laps=False)

    if config['DEFAULT']['pickle_output'].strip().lower() == 'true':
        pickle_data(all_behaviroual_data, config['DEFAULT']['pickle_output_path'])