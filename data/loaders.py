import pandas as pd
import numpy as np
import h5py
import os
import configparser


class Day0to6_Loader:
    def __init__(self, config: configparser):
        self.config = config
        self.mouse_metadata: pd.DataFrame = self._get_mouse_metadata_df(root_folder=config['DEFAULT']['data_root'],
                                                                        replace_str=config['DEFAULT'][
                                                                            'replace_path_str'])
        self.unsplit_behavioural_data = None
        self.split_behavioural_data = None

    def get_all_behavioural_data_dict(self, split_laps: bool) -> dict:
        """
        Returns a dict indexed by mouse_id, with values = either 1 data frame per mouse, or 1 DF per mouse-lap
        :param split_laps: bool, if false, returns one df with all the laps of the mouse
        :return: a dictionary of dataframes or a dictionary with a list of dataframes
        """
        if split_laps:
            split_laps_data = {x[0]: self._split_mouse_runs(self._load_h5py_file(x[1])) for x in
                               self.mouse_metadata[['mouse_id', 'filename']].values}
            self.split_behavioural_data = split_laps_data
            return split_laps_data
        else:
            all_laps_data = {x[0]: self._load_h5py_file(x[1]) for x in
                             self.mouse_metadata[['mouse_id', 'filename']].values}
            self.unsplit_behavioural_data = all_laps_data
            return all_laps_data

    def get_behavioural_data_subset(self, mouse_ids: list = None, days: list = None, groups: list = None,
                                    filenames: list = None, invert_selection=False, split_laps=False):
        def fix_if_not_list(list_to_check):
            if list_to_check is None:
                return None
            if not isinstance(list_to_check, list):
                return [list_to_check]

        def subset_metadata(df: pd.DataFrame, column_name: str, subset_values: list, invert_selection: bool):
            if invert_selection:
                return df[~df[column_name].isin(subset_values)]
            else:
                return df[df[column_name].isin(subset_values)]

        mouse_ids = fix_if_not_list(mouse_ids)
        days = fix_if_not_list(days)
        groups = fix_if_not_list(groups)
        filenames = fix_if_not_list(filenames)

        metadata_subset = self.mouse_metadata.copy()
        if mouse_ids is not None:
            metadata_subset = subset_metadata(metadata_subset, 'mouse_id', mouse_ids,
                                              invert_selection)  # metadata_subset[metadata_subset.mouse_id.isin(mouse_ids)]
        if days is not None:
            metadata_subset = subset_metadata(metadata_subset, 'day', days, invert_selection)
        if groups is not None:
            metadata_subset = subset_metadata(metadata_subset, 'group', groups, invert_selection)
        if filenames is not None:
            metadata_subset = subset_metadata(metadata_subset, 'filename', filenames, invert_selection)

        return self.get_all_behavioural_data_dict(mouse_metadata=metadata_subset, split_laps=split_laps)

    def _get_mouse_metadata_df(self, root_folder: str, replace_str: str = None):
        """
        Given the root folder, it explores all subdirectories and gives a data frame with the metadata for each mouse, and
        the filepath to its data.
        :param root_folder: The root folder of the file path. See config file for details.
        :param replace_str: Just a way to make the resulting pandas data frame a bit prettier. Replaces the path prefix to
        the root directory that contains all the data files within subfolders. Default - root-folder if None.
        :return: DataFrame with the metadata (incl. filepaths) to all mice.
        """
        if replace_str is None:
            replace_str = root_folder

        fileinfo = []
        for path, subdirs, files in os.walk(root_folder):
            for file in files:
                if file.find(".h5") > 0:
                    file_path = path + "/" + file
                    path = path.replace(replace_str, "")
                    m_type, day, group, mouse_id = path.split("/")
                    fileinfo.append([mouse_id, m_type, group, day, file_path])
        mouse_data = pd.DataFrame(fileinfo, columns=["mouse_id", "type", "group", "day", "filename"])
        return mouse_data

    def _load_h5py_file(self, filepath):
        """
        Reads the h5py file with the behavioural data
        :param filepath: Path to file
        :return: DataFrame with the behavioural data
        """
        return pd.read_hdf(filepath)

    def _split_mouse_runs(self, df: pd.DataFrame, ignore_first_lap: bool = True, ignore_truncated_first_lap: bool = True, ignore_truncated_first_lap_threshold = 50):
        """
        Takes the behavioural data, and splits into an array of DataFrames. Each item in the list is one run of the
        treadmill (0-360cm)
        :param df: DataFrame with the behavioural data. Assumed that the position column changing by more than 100cm in one
        time step signifies a new "lap".
        :return: list of DataFrame objects, one per lap.
        """
        dfs = []

        n_laps = int(df['Laps'].max() + 1)
        if ignore_first_lap:
            for i in range(1,n_laps):
                dfs.append(df[df['Laps']==i])
        elif ignore_truncated_first_lap:
            if df.iloc[0]['Position_cm'] > ignore_truncated_first_lap_threshold:
                skip_first_lap = True
            if skip_first_lap:
                for lap in range(1,n_laps):
                    dfs.append(df[df['Laps'] == lap])
            else:
                for lap in range(n_laps):
                    dfs.append(df[df['Laps'] == lap])

        return dfs


if "__name__" == "__main__":
    print("this file is not meant to be run. Please use the functions in your own scripts instead.")
