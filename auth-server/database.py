from fastapi import FastAPI, Request #FAST api used to create web application and define routes, Request represnets an incoming HTTP reuqest froma. client
from fastapi.responses import HTMLResponse #allows you to return html as an HTTP response
from fastapi.staticfiles import StaticFiles #allows FAST API to serve static files, CSS files, JS files, images ->backend serves directly than generating dynamically
from fastapi.templating import Jinja2Templates #connects FAST api with Jinja2 templating engine, alows backend to load html files and dyubamically inser info into them 

import os #python access environemtn variables and OS functinoality 
import psycopg #connect and communicate with postgreSQL

from contextlib import asynccontextmanager #define a function that manages startup and shutdown operation for FASTAPI
from dotenv import load_dotenv #loads variables from .env file into python environemnt variables 
import uuid
load_dotenv()

DATABASE_URL = (f"postgresql://{os.getenv('LOCAL_USER')}:"
    f"{os.getenv('LOCAL_PASSWORD')}@postgres:5432/"
    f"{os.getenv('LOCAL_DB')}")

def initialize_databse():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_accounts (
                    id UUID PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(100) NOT NULL
                )
            """)
        conn.commit()
        


def get_user_by_username(username: str):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM user_accounts WHERE username = %s", (username,)) #user[0] = userid, user[1] = username, user[2] = passwordhash
            user = cursor.fetchone() #retrieves the first matching row 
            return user
        
def create_user(username: str, password: str):
    userid = str(uuid.uuid4())
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO user_accounts (id, username, password) VALUES (%s, %s, %s)", (userid, username, password))
        conn.commit()