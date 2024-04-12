# Fast API
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

#dotenv
from dotenv import load_dotenv

# database
from database.config import engine, Base
# middlewares
from middlewares.error_handler import ErrorHandler
# routers
from routers.movie import movie
from routers.auth import auth


load_dotenv()


app = FastAPI()
app.title = "My app backend with FastAPI"
app.version = "0.0.1"
app.description = "This is a simple app backend with FastAPI"
app.contact = {
    "name": "Carlos Argelio Palacios Ramos",
    "url": "https://www.linkedin.com/in/palaciosrcarlosa/",
    "email": "carlosargelio0104@gmail.com",
}

app.debug = True # False default ( This need enviroment configuration )

app.add_middleware(ErrorHandler)

# create tables

Base.metadata.create_all(bind=engine)

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')

app.include_router(auth)
app.include_router(movie)