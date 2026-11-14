from fastapi import FastAPI, Request #FAST api used to create web application and define routes, Request represnets an incoming HTTP reuqest froma. client
from fastapi.responses import HTMLResponse #allows you to return html as an HTTP response
from fastapi.staticfiles import StaticFiles #allows FAST API to serve static files, CSS files, JS files, images ->backend serves directly than generating dynamically
from fastapi.templating import Jinja2Templates #connects FAST api with Jinja2 templating engine, alows backend to load html files and dyubamically inser info into them 

app = FastAPI() #main object that manages the backend

app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")
app.mount("/images", StaticFiles(directory="images"), name="images")
templates = Jinja2Templates(directory="pages")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="homepage.html",
        context = {}
    )

@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context = {}
    )
    
@app.get("/register")
async def register(request: Request):
    return templates.TemplateResponse(request=request, name="register.html", context = {})