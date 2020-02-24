from fastapi import FastAPI
gigscovery_app = FastAPI()

@gigscovery_app.get("/")
async def root():
    return {"message": " Gigscovery API"}

@gigscovery_app.get("/users/me")
async def read_user_me():
    return {"user_id": "Natasha"}


@gigscovery_app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": 1508}

@gigscovery_app.get("/model/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "We are awesome"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
        return {"model_name": model_name, "message": "Have some residuals"}
