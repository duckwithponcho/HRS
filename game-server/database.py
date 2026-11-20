from fastapi import FastAPI, Request #FAST api used to create web application and define routes, Request represnets an incoming HTTP reuqest froma. client
from fastapi.responses import HTMLResponse #allows you to return html as an HTTP response
from fastapi.staticfiles import StaticFiles #allows FAST API to serve static files, CSS files, JS files, images ->backend serves directly than generating dynamically
from fastapi.templating import Jinja2Templates #connects FAST api with Jinja2 templating engine, alows backend to load html files and dyubamically inser info into them 

import os #python access environemtn variables and OS functinoality 
import psycopg #connect and communicate with postgreSQL

from contextlib import asynccontextmanager #define a function that manages startup and shutdown operation for FASTAPI
from dotenv import load_dotenv #loads variables from .env file into python environemnt variables 

DATABASE_URL = (f"postgresql://{os.getenv('LOCAL_USER')}:"
    f"{os.getenv('LOCAL_PASSWORD')}@postgres:5432/"
    f"{os.getenv('LOCAL_DB')}")


def initialize_database():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS games (
                    id SERIAL PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        conn.commit()