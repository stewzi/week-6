import os
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().with_name(".env"))


class Genius:
    def __init__(self, access_token):
        self.access_token = access_token

    def _get(self, path, params=None):
        """Request data from the Genius API."""
        response = requests.get(
            "https://api.genius.com" + path,
            headers={"Authorization": "Bearer " + self.access_token},
            params=params,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["response"]

    def get_artist(self, search_term):
        """Find the primary artist of the first search result."""
        data = self._get("/search", params={"q": search_term})
        hits = data["hits"]
        if not hits:
            return {}

        artist_id = hits[0]["result"]["primary_artist"]["id"]
        artist_data = self._get(f"/artists/{artist_id}")
        return artist_data["artist"]

    def get_artists(self, search_terms):
        """Return one row of artist information for each search term."""
        rows = []
        for search_term in search_terms:
            artist = self.get_artist(search_term)
            rows.append({
                "search_term": search_term,
                "artist_name": artist.get("name"),
                "artist_id": artist.get("id"),
                "followers_count": artist.get("followers_count"),
            })

        return pd.DataFrame(rows, columns=[
            "search_term", "artist_name", "artist_id", "followers_count"
        ])
