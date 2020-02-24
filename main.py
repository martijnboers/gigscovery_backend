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
