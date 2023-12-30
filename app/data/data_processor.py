import pandas as pd
from collections import defaultdict

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