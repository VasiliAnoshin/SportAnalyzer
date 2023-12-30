from fastapi import FastAPI, Query, HTTPException
import sys
from pathlib import Path
from dotenv import load_dotenv
sys.path.append(Path(__file__).parents[1].as_posix())
from app.data.data_loader import DataLoader
from app.data.data_processor import DataProcessor
import redis
load_dotenv()
import time

app = FastAPI()
DATA_FILE = "inventory_lsports-dev_full_14_03_2023_sample1M.parquet"

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Save data to Redis during startup
@app.on_event("startup")
async def startup_event():
    try:
        app.state.redis_client = redis.StrictRedis(host="localhost", port=6379)
        if not app.state.redis_client.exists("games"):
            all_games_df = DataLoader(DATA_FILE).load()
            print(all_games_df)
            app.state.redis_client.set("games", all_games_df.to_json(orient='records'))
            print("Data saved in Redis db successfully.")
    except Exception as ex:
        print(f"Error saving to Redis: {ex}")

@app.get("/list_all_games")
def list_of_all_games():
    start_time = time.time() #Record the start time
    try:
        all_games_df = DataLoader(DATA_FILE).load()
        list_of_games = DataProcessor(all_games_df).get_list_of_games()
        return {"all_games": list(list_of_games)}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    finally:
        end_time = time.time()  # Record the end time
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")

@app.get("/list_total_games_by_sport")
def get_games_count_per_sport(sport: str = Query(None, description="Filter games by sport")):
    start_time = time.time() #Record the start time
    try:
        all_games_df = DataLoader(DATA_FILE).load()
        games_total = DataProcessor(all_games_df).get_games_count_per_sport(sport)
        return {sport: games_total}
    except KeyError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    finally:
        end_time = time.time()  # Record the end time
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")

@app.get("/get_representative_data")
def get_representative_data(sportName:str, frameCount:int, fixturesCount:int):
    ...