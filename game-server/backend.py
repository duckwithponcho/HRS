from fastapi import FastAPI, Request #FAST api used to create web application and define routes, Request represnets an incoming HTTP reuqest froma. client
from fastapi.responses import HTMLResponse #allows you to return html as an HTTP response
from fastapi.staticfiles import StaticFiles #allows FAST API to serve static files, CSS files, JS files, images ->backend serves directly than generating dynamically
from fastapi.templating import Jinja2Templates #connects FAST api with Jinja2 templating engine, alows backend to load html files and dyubamically inser info into them 
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse

import os #python access environment variables and OS functionality 
import psycopg #connect and communicate with postgreSQL
import database

from contextlib import asynccontextmanager #define a function that manages startup and shutdown operation for FASTAPI
from dotenv import load_dotenv #loads variables from .env file into python environemnt variables 
from auth import verify_jwt #import the verify_jwt function from auth.py
import bcrypt

#NOTE: Keep hompage, game routes, and other application functiaonltiy in game-server/backend.py

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):

    database.createGameRoomTable()

    yield


app = FastAPI(lifespan=lifespan)


app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")
app.mount("/images", StaticFiles(directory="images"), name="images")
templates = Jinja2Templates(directory="pages")    

@app.get("/")
async def home(request: Request):
    username = get_current_username(request)
    return templates.TemplateResponse(
        request=request,
        name="homepage.html",
        context = {"username":username}
    )
    
@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"username": get_current_username(request)})

@app.get("/register")
async def register(request: Request):
    return templates.TemplateResponse(request=request, name="register.html", context={"username": get_current_username(request)})

@app.get("/lobby")
async def lobby(request: Request):
    with database.get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                           SELECT roomName, playerNames, gameStarted FROM gameRooms
                           ORDER BY
                           CASE
                           WHEN CARDINALITY(playerNames) = 10 THEN 2
                           ELSE 1
                           END ASC,
                           CARDINALITY(playerNames) DESC
                           """)
            rooms = cursor.fetchall()
            return templates.TemplateResponse(request=request, name="lobby.html", context={
                "username": get_current_username(request),
                "rooms": rooms})

# @app.get("/lobby")
# async def lobby(request: Request):
#     return templates.TemplateResponse(request=request, name="lobby.html", context={"username": get_current_username(request)})

@app.get("/create-room")
async def createRoom(request: Request):
    return templates.TemplateResponse(request=request, name="createRoom.html", context={"username": get_current_username(request)})

@app.get("/your-room")
async def renderYourRoom(request: Request, roomName: str):
    return templates.TemplateResponse(request=request, name="yourRoom.html", context={"username": get_current_username(request), 
    "roomName": roomName})

@app.post("/your-room")
async def yourRoom(request: Request):
    formData = await request.form()
    roomName = formData.get("roomName")
    with database.get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM gameRooms WHERE roomName = %s", (roomName,))
            room = cursor.fetchone()
            if len(roomName) > 20:
                return JSONResponse(status_code = 400, content = {"error": "Room Name Length Requirement not met"})
            elif room is None:
                cursor.execute("INSERT INTO gameRooms (roomName, playerNames) VALUES (%s, %s)", (roomName, [get_current_username(request)]))
            elif room is not None:
                return JSONResponse(status_code = 400, content = {"error": "Room exists already!"})

    return RedirectResponse(url="/your-room?roomName=" + roomName, status_code=303)

def get_current_username(request: Request):
    token = request.cookies.get("auth_token")
    if not token:
        return None
    
    payload = verify_jwt(token)
    
    if payload is None:
        return None
    return payload.get("sub")

