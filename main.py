# ! pip install fastapi

from fastapi import FastAPI
from enum import Enum
from functions.spotify_connectors import name, user_artists

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