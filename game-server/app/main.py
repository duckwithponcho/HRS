from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Game server is running!"}