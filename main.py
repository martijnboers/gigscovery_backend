# ! pip install fastapi

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from enum import Enum
from functions.spotify_connectors import name, user_artists, user_track_features
from functions.bit_connectors import  get_concerts, get_artist_concerts
from functions.clustering import get_bins


gigscovery_app = FastAPI()

origins = [
    "https://scoaring.com",
    "https://www.scoaring.com",
    "http://127.0.0.1:8000/",
    "http://localhost",
    "http://localhost:8000"
]


gigscovery_app.add_middleware(
    CORSMiddleware,
    allow_origins=[origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

#ENDPOINT 1: USERS ARTIST (TOP + RELATED)
@gigscovery_app.get("/artists/get_user_artists")
async def user_artists_endpoint(token: str, n_of_top_artists: int = 5, n_related_artists : int = 5):
    return {"users_artists": user_artists(n_of_top_artists, n_related_artists, token)}

#ENDPOINT 2: USER'S TRACKs FEATURE SPACE
@gigscovery_app.get("/tracks/features")
async def tracks_features_endpoint(token: str, n_of_top_artists: int = 5, n_related_artists : int = 5):
    return {"audio_features": user_track_features(n_of_top_artists, n_related_artists, token)}


