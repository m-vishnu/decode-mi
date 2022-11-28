# Code for loading the behavioural data

#### How to run:

1) Run the config.py file with the data_root folder specified correctly. This will create the config file in the root
   folder of the project.
2) Run main.py, it creates a dictionary with one key for each "mouse_id" for which behavioural data was found. The key
   indexes a list of DataFrame objects, one for each lap run by the mouse.

#### Prerequisites:

1. Install all the necessary packages listed in requirements.txt (e.g:, run command pip install -r requirements.txt)
2. Please create a folder "intermediate_files/processed_data" in the root folder of the project. (e.g: There will be the
   folders 'data', 'intermediate_files', and the 'venv' folder that you set up in the project root.)