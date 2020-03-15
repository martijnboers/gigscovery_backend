

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from functions.spotify_connectors import user_artists, user_track_features
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

# @gigscovery_app.get("/")
# async def root():
#     return {"message": " Gigscovery API"}


# @gigscovery_app.get("/user_artists/{n_artists}")
# async def user_artists_endpoint(n_artists: int):
#     return {"users_artists": user_artists(n_artists)}


# #ENDPOINT BiT: GET CONCERTS
# @gigscovery_app.get("/get_concerts/")
# async def get_concerts_endpoint(artist: str, latitude: str, longitude: str, date_begin: str, date_end: str):
#     return {"get_concerts": get_concerts(latitude, longitude, date_begin, date_end, artist)}


#ENDPOINT 1: USERS ARTIST (TOP + RELATED)
@gigscovery_app.get("/artists/get_user_artists")
async def user_artists_endpoint(token: str, n_of_top_artists: int = 5, n_related_artists : int = 5):
    return {"users_artists": user_artists(n_of_top_artists, n_related_artists, token)}


#ENDPOINT 2: USER'S TRACKs FEATURE SPACE
@gigscovery_app.get("/tracks/features")
async def tracks_features_endpoint(token: str, n_of_top_artists: int = 5, n_related_artists : int = 5):
    return {"audio_features": user_track_features(n_of_top_artists, n_related_artists, token)}


@gigscovery_app.get("/get_bins")
async def get_bins_endpoint(latitude: float, longitude: float, date_begin: str, date_end: str, token: str, radius: int = 150, top_artists: int = 10, related_artists: int =5):
    return {"user_bins": get_bins(latitude, longitude, date_begin, date_end, token, radius, top_artists, related_artists)}

