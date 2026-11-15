from fastapi import FastAPI, Request, HTTPException #FAST api used to create web application and define routes, Request represnets an incoming HTTP reuqest froma. client


import os #python access environemtn variables and OS functinoality 
import psycopg #connect and communicate with postgreSQL

from contextlib import asynccontextmanager #define a function that manages startup and shutdown operation for FASTAPI
from dotenv import load_dotenv #loads variables from .env file into python environemnt variables 

import jwt
from datetime import datetime, timedelta, timezone
from database import initialize_databse, get_user_by_username,create_user
import bcrypt
import html

from fastapi.responses import RedirectResponse

load_dotenv()

with open("keys/private.pem","r") as key_file:
    PRIVATE_KEY = key_file.read()

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_databse()
    yield
    
app = FastAPI(lifespan=lifespan) #main object that manages the backend

#clear authentication cookie
@app.post("/logout")
async def logout(request:Request):
   response = RedirectResponse(url="/login", status_code=302)
   response.delete_cookie(key="auth_token", path="/")
   return response


#Create new account
@app.post("/register")
async def register_post(request: Request):
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")
    
    #validate username and password here
    
    #check if username is already taken
    if get_user_by_username(username) is not None:
        raise HTTPException(status_code=400, detail = "user already exists")
    if not verify_username(username):
        raise HTTPException(status_code=400, detail="Invalid username")
    if not verify_password(password):
        raise HTTPException(status_code=400, detail="Invalid password")
    username = html.escape(username)
    
    
    
    hashed_password = hash_password(password)
    create_user(username, hashed_password)
    return {"message": f"User created successfully: {username}"}

@app.post("/login")
async def login(request: Request):
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")

    user = get_user_by_username(username)

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    stored_hash = user[2]
    token = generate_jwt(user[1])
    print(user[1])
    if not check_password(password, stored_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    response = RedirectResponse(url="/",status_code=303)
    
    response.set_cookie(key="auth_token",value = token, httponly=True,secure=False,samesite="lax",max_age=3600,path="/")
    return response

def generate_jwt(username: str):
    payload = {
        "sub":username,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    
    token = jwt.encode(payload, PRIVATE_KEY,algorithm="RS256")
    
    return token

#make sure that the username is valid and not already taken
def verify_username(username: str):
    if not username:
        return False
    #make sure username only contains alphanumeric 
    if not username.isalnum():
        return False
    
    if len(username) < 3 or len(username) > 20:
        return False
    return True

#verify the password is long and complicated enough
SPECIAL_CHARACTERS = "!@#$%^&()-_="
def verify_password(password: str):
    if len(password) < 8:
        return False
    for char in password:
        if not char.isalnum() and char not in SPECIAL_CHARACTERS:
            return False
    return True


def hash_password(password: str):
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    
    return hashed_password.decode("utf-8")

def check_password(password: str, stored_hash: str):
    password_bytes = password.encode("utf-8")
    stored_hash_bytes = stored_hash.encode("utf-8")
    
    return bcrypt.checkpw(password_bytes, stored_hash_bytes)
    