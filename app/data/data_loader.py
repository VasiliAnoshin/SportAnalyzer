import os
import pandas as pd

class DataLoader:
    def __init__(self, file_name:str):
        self.file_name = file_name
    
    def get_file_path(self, relative_path:str) ->str:
        """
        Prepare the absolute file path based on the current script's directory and a relative path.

        Parameters:
        - relative_path (str): The relative path to the file.

        Returns:
        - str: The absolute file path.
        """
        # Get the directory of the current script
        current_directory = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_directory, relative_path)

    def load(self)->pd.DataFrame:
        """
        Load data from a Parquet file.

        Returns:
        - pd.DataFrame: Loaded data as a Pandas DataFrame.
        
        Raises:
        - Exception: If the file does not exist.
        """
        file_path = self.get_file_path(self.file_name)
        # Load data during server initialization
        if os.path.exists(file_path):
            data_file_path = file_path
            games_data = pd.read_parquet(data_file_path)
            return games_data
        else:
            raise Exception(f'The file {file_path} does not exist.')