import requests
import json
from pathlib import Path
import pandas as pd

def getNews():
    configPath = Path(__file__).with_name('config.json')
    configJson = pd.read_json(configPath)

    url = (f"https://newsapi.org/v2/top-headlines?country=de&apiKey={configJson['urls&token']['newsapiToken']}")
    df = requests.get(url).json()
    with open(Path(__file__).with_name('data.json'), 'w', encoding='utf-8') as f:
        json.dump(df, f, ensure_ascii=False, indent=4)