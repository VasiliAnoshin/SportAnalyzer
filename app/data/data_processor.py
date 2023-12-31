import pandas as pd
from collections import defaultdict
import numpy as np

class DataProcessor:
    def __init__(self, all_games_df:pd.DataFrame) -> None:
        self.games_df= all_games_df

    def get_list_of_games(self)->list:
        """
        Get a list of unique sports from the DataFrame.

        Returns:
        - list: A list containing unique sports extracted from the "key" column.

        Example:
            ['Volleyball', 'Tennis', 'Soccer', ...]
        """
        unique_sports = set()
        for game_entry in self.games_df["key"]:
            title  = game_entry.partition("/")[0]
            if title and title not in unique_sports:
                unique_sports.add(title)
        return unique_sports

    def get_games_count_per_sport(self, sport:str) ->dict:
        """
        Count the number of games associated with a specific sport in the DataFrame.
        
        Args:
        - sport (str): The sport for which to count the number of games.
        
        Returns:
        - int: The count of games associated with the specified sport.
        
        Raises:
        - KeyError: If there are no games associated with the specified sport.
        """
        try:
            count = 0
            for game_entry in self.games_df["key"]:
                game = game_entry.partition("/")[0]
                if game != "" and game == sport:
                    count+=1
            if count == 0:
                raise KeyError(f"There is no such sport -[ {sport} ]. Try to select available sport from list_all_games endpoint.")
            return count
        except AttributeError as e:
            print(f"Check input data: dataframe or [key] header is not available: {e}")
            raise
        except IndexError as e:
            print(f"Can't split input_data entry, partition returns fewer than 3 parts: {e}")
            raise

    def get_representative_data(self, sport_name: str, frame_count: int, fixtures_count: int) -> list[str]:
        """
        Get a representative dataset for a specific sport.

        Args:
        - df (pd.DataFrame): The DataFrame containing the original dataset.
        - sport_name (str): The name of the sport for which to fetch the dataset.
        - frame_count (int): The number of frames.
        - fixtures_count (int): The number of random games to consider.

        Returns:
        - list[str]: A list of keys representing the representative dataset.

        Raises:
        - ValueError: If the specified sport is not present in the DataFrame.

        Example:
        >>> df = pd.read_csv("your_dataset.csv")
        >>> get_representative_data(df, "Soccer", 100, 200)
        ['Soccer/204/123/Frames/123_20230101.png', 'Soccer/204/456/Frames/456_20230102.png', ...]
        """
        try:
            if frame_count > fixtures_count:
                raise ValueError('Frame count cant be > fixtures_count')
            filtered_set = set()
            for game_entry in self.games_df["key"]:
                game = game_entry.partition("/")[0]
                if game and game == sport_name:
                    filtered_set.add(game_entry)
            # Fetch random fixtures
            random_fixtures = np.random.choice(list(filtered_set), size=min(fixtures_count, len(filtered_set)), replace=False)
            random_frames = np.random.choice(random_fixtures, size=len(random_fixtures), replace=False)
            return list(random_frames)
        except Exception as ex:
            raise ex