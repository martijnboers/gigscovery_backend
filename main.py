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

@gigscovery_app.get("/filter_concert_location/{city, concert_list}")
async def filter_concert_location(city: str, concert_list: int):
    return {"filter_concert_location": filter_concert_location(city, concert_list)}

@gigscovery_app.get("/get_concerts/{location, date, artist}")
async def get_concerts(location: str, date: int, artist: str):
    return {"get_concerts": get_concerts(location, date, artist)}
