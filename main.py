from fastapi import FastAPI
gigscovery_app = FastAPI()

@gigscovery_app.get("/")
async def root():
    return {"message": " Gigscovery API"}
