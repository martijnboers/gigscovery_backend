# ! pip install fastapi

from fastapi import FastAPI
from enum import Enum
from functions.spotify_connectors import name, user_artists
from functions.bit_connectors import  get_concerts, get_artist_concerts

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
async def user_artists_endpoint(n_artists: int):
    return {"users_artists": user_artists(n_artists)}


#ENDPOINT BiT: GET CONCERTS
@gigscovery_app.get("/get_concerts/")
async def get_concerts_endpoint(artist: str, latitude: str, longitude: str, date_begin: str, date_end: str):
    return {"get_concerts": get_concerts(latitude, longitude, date_begin, date_end, artist)}
