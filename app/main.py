from fastapi import FastAPI, Query, HTTPException
import sys
from pathlib import Path
from dotenv import load_dotenv
sys.path.append(Path(__file__).parents[1].as_posix())
from app.data.data_loader import DataLoader
from app.data.data_processor import DataProcessor
from functools import wraps
load_dotenv()
import time

app = FastAPI()
DATA_FILE = "inventory_lsports-dev_full_14_03_2023_sample1M.parquet"

@app.get("/")
def read_root():
    return {"Hello": "World"}


def calculate_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Record the start time
        try:
            result = func(*args, **kwargs)
            return result
        except KeyError as ex:
            raise HTTPException(status_code=404, detail=str(ex))
        except Exception as ex:
            raise HTTPException(status_code=500, detail=str(ex))
        finally:
            end_time = time.time()  # Record the end time
            execution_time = end_time - start_time
            print(f"Execution time: {execution_time} seconds")
    return wrapper

@app.get("/list_all_games")
@calculate_execution_time
def list_of_all_games():
    """
    Get the list of all unique sports available in the dataset.

    Returns:
    - Dict: A dictionary containing the key "all_games" and a list of all unique sports.

    Raises:
    - HTTPException: If there is an error processing the request.

    Example:
    ```python
    # Request example
    curl -X 'GET' \
      'http://localhost:8008/list_all_games' \
      -H 'accept: application/json'

    # Response example
    {
      "all_games": [
        "Volleyball",
        "Tennis",
        "Soccer",
        ...
      ]
    }
    ```
    """
    all_games_df = DataLoader(DATA_FILE).load()
    list_of_games = DataProcessor(all_games_df).get_list_of_games()
    return {"all_games": list(list_of_games)}


@app.get("/list_total_games_by_sport")
@calculate_execution_time
def get_games_count_per_sport(sport: str = Query(None, description="Filter games by sport")):
    """
    Get the total number of games for the specified sport.

    Parameters:
    - sport (str): The sport name to filter games. If not provided, returns the total number of games for all sports.

    Returns:
    - Dict: A dictionary containing the sport name (or 'all_sports') and the total number of games.

    Raises:
    - HTTPException: If there is an error processing the request.
    """
    all_games_df = DataLoader(DATA_FILE).load()
    games_total = DataProcessor(all_games_df).get_games_count_per_sport(sport)
    return {sport: games_total}

@app.get("/get_representative_data")
@calculate_execution_time
def get_representative_data(
    sportName: str = Query(..., description="Name of the sport"),
    frameCount: int = Query(..., description="Number of frames to fetch for each fixture"), 
    fixturesCount: int = Query(..., description="Number of fixtures to select")):
    """
    Get a representative dataset for the specified sport.

    Parameters:
    - sportName (str): Name of the sport.
    - frameCount (int): Number of frames to fetch for each selected fixture.
    - fixturesCount (int): Number of fixtures to randomly select.

    Returns:
    - Dict: A dictionary containing the sport name and a list of representative frames.

    Raises:
    - HTTPException: If there is an error processing the request.
    """
    all_games_df = DataLoader(DATA_FILE).load()
    repr_data = DataProcessor(all_games_df).get_representative_data(sportName, frameCount, fixturesCount)
    return {sportName: repr_data}