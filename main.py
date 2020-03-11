# ! pip install fastapi

from fastapi import FastAPI
from enum import Enum
from functions.spotify_connectors import name, user_artists
from functions.bit_connectors import filter_concert_location, get_concerts

gigscovery_app = FastAPI()


@gigscovery_app.get("/")
async def root():
    return {"message": " Gigscovery API"}


@gigscovery_app.get("/users/me")
async def read_user_me():
    return {"user_id": name()}


@gigscovery_app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": 1508}

@gigscovery_app.get("/user_artists/{n_artists}")
async def user_artists(n_artists: int):
    return {"users_artists": user_artists(n_artists)}

@gigscovery_app.get("/prune_concerts/")
async def prune_concerts(concert_list: str):
    return {"prune_concerts": prune_concerts(concert_list)}

@gigscovery_app.get("/get_artist_concerts/{artist_name, date_range}")
async def get_artist_concerts(artist_name: str, date_range: str):
    return {"get_artist_concerts": get_artist_concerts(artist_name, date_range)}

@gigscovery_app.get("/filter_concert_location/{city, concert_list}")
async def filter_concert_location(city: str, concert_list: str):
    return {"filter_concert_location": filter_concert_location(city, concert_list)}
#ENDPOINT BiT: GET CONCERTS
@gigscovery_app.get("/get_concerts/")
async def get_concerts_endpoint(location: str, date: str="2020-01-02, 2020-04-01", artist: str):
    return {"get_concerts": get_concerts(location, date, artist)}
