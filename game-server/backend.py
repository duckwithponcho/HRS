from fastapi import FastAPI, Request #FAST api used to create web application and define routes, Request represnets an incoming HTTP reuqest froma. client
from fastapi.responses import HTMLResponse #allows you to return html as an HTTP response
from fastapi.staticfiles import StaticFiles #allows FAST API to serve static files, CSS files, JS files, images ->backend serves directly than generating dynamically
from fastapi.templating import Jinja2Templates #connects FAST api with Jinja2 templating engine, alows backend to load html files and dyubamically inser info into them 

import os #python access environemtn variables and OS functinoality 
import psycopg #connect and communicate with postgreSQL

from contextlib import asynccontextmanager #define a function that manages startup and shutdown operation for FASTAPI
from dotenv import load_dotenv #loads variables from .env file into python environemnt variables 
from auth import verify_jwt #import the verify_jwt function from auth.py
import bcrypt

#NOTE: Keep hompage, game routes, and other application functiaonltiy in game-server/backend.py

load_dotenv()
from database import initialize_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
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
    return templates.TemplateResponse(request=request, name="login.html",context={"username": get_current_username(request)})

@app.get("/register")
async def register(request: Request):
    
    return templates.TemplateResponse(request=request, name="register.html", context={"username": get_current_username(request)})


def get_current_username(request: Request):
    token = request.cookies.get("auth_token")
    if not token:
        return None
    
    payload = verify_jwt(token)
    
    if payload is None:
        return None
    return payload.get("sub")