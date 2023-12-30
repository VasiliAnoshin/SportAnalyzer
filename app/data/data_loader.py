import os
import pandas as pd

class DataLoader:
    def __init__(self, data_file:str):
        self.file_path = data_file
    
    def load(self):
        # Get the directory of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # # Build the relative path to the 'data' folder
        # data_folder = os.path.join(current_directory, 'data')
        file_path = os.path.join(current_directory, self.file_path)
        # Load data during server initialization
        if os.path.exists(file_path):
            data_file_path = file_path
            games_data = pd.read_parquet(data_file_path)
            print(games_data)
            return games_data
        else:
            raise Exception(f'The file {file_path} does not exist.')