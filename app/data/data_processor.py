import pandas as pd
from collections import defaultdict

class DataProcessor:
    def __init__(self, all_games_df:pd.DataFrame) -> None:
        self.games_df= all_games_df

    def get_list_of_games(self):
        output = set()
        for game in self.games_df["key"]:
            res = game.partition("/")[0]
            if res not in output and res != "":
                output.add(res)
        return output

    def get_games_count_per_sport(self) ->dict:
        try:
            game_col = defaultdict(int)
            for game_entry in self.games_df["key"]:
                game = game_entry.partition("/")[0]
                if game != "":
                    game_col[game] +=1
            return game_col
        except AttributeError as e:
            print(f"Check input data: dataframe or [key] header is not available: {e}")
            raise
        except IndexError as e:
            print(f"Can't split input_data entry, partition returns fewer than 3 parts: {e}")
            raise