# pau/services/search_service.py

import requests
from pau.config import Config


def perform_search(query):
    params = {"q": query, "format": "json"}
    headers = {"User-Agent": "Mozilla/5.0 (compatible; PAU/1.0)"}
    resp = requests.get(Config.SEARXNG_API_URL, params=params, headers=headers)
    resp.raise_for_status()
    return resp.json()
