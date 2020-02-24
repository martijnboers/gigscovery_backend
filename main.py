from fastapi import FastAPI
from enum import Enum
from functions.spotify_connectors import name, give_top_artists

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


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@gigscovery_app.get("/model/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}



@gigscovery_app.get("/top_artists/{number_of_artists}")
async def get_top_artists(number_of_artists: int):
    return {"top_artists": give_top_artists(number_of_artists)}