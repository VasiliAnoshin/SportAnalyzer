from fastapi import FastAPI, Query
import pandas as pd
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
sys.path.append(Path(__file__).parents[1].as_posix())
from app.data.data_loader import DataLoader

import redis
load_dotenv()

app = FastAPI()
DATA_FILE = os.getenv("DATA_FILE")

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Save data to Redis during startup
@app.on_event("startup")
async def startup_event():
    try:
        all_games_df = DataLoader(DATA_FILE).load()
        print(all_games_df)
    except Exception as ex:
        print(f"Error saving to Redis: {ex}")

@app.get("/list_all_games")
def get_games_count_per_sport():
    ...

@app.get("/list_games_by_sport")
def get_games_count_per_sport(sport: str = Query(None, description="Filter games by sport")):
    ...

@app.get("/get_representative_data")
def get_representative_data(sportName:str, frameCount:int, fixturesCount:int):
    ...