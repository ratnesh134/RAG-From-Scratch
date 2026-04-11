import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH_MOVIES = PROJECT_ROOT/'data'/'movies.json'
DATA_PATH_STOPWORDS = PROJECT_ROOT/'data'/'stopwords.txt'
CACHE_PATH = PROJECT_ROOT/'cache'

def load_movies() -> list[dict]:
    with open(DATA_PATH_MOVIES, 'r') as f:
        data = json.load(f)
    
    return data['movies']

def load_stopwords():
    with open(DATA_PATH_STOPWORDS,"r") as f:
        data = f.read().splitlines()
    
    return data