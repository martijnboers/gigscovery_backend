# ! pip install fastapi

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from enum import Enum
from functions.spotify_connectors import name, user_artists

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


<<<<<<< HEAD
#ENDPOINT 1: USERS ARTIST (TOP + RELATED)
@gigscovery_app.get("/artists/{user_artists}")
async def user_artists(n_of_top_artists: int = 5, n_related_artists : int = 5):
    return {"users_artists": user_artists(n_artists)}

#ENDPOINT 2: 

=======
@gigscovery_app.get("/user_artists/{n_artists}")
async def user_artists(n_artists: int):
    return {"users_artists": user_artists(n_artists)}

>>>>>>> 28b6d0f4889d45fc4f9be40f0ff747c6ffde8eb3
