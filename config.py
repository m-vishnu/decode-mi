import configparser

config = configparser.ConfigParser()
config['DEFAULT'] = {
    'data_root': "/home/mvishnu/Documents/work/DECODE/data/Day0to6/",
    'replace_path_str': "/home/mvishnu/Documents/work/DECODE/data/Day0to6/",
    'split_mouse_laps': 'True',
    'pickle_output': 'True',
    'pickle_output_path': './intermediate_files/processed_data/mouse_laps.pkl'
}

def write_config_data():
    print("Committing configuration to config file.")
    with open("./config", 'w') as config_file:
        config.write(config_file)

if __name__ == "__main__":
    write_config_data()
