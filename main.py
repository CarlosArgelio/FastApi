# Python
from typing import Optional, List

# Fast API
from fastapi import FastAPI, Request, Depends
from fastapi import HTTPException
from fastapi import Path, Query, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
# Pydantic
from pydantic import BaseModel, Field
#dotenv
from dotenv import load_dotenv

# internal
from jwt_manager import create_token, validate_token
from database.config import session, engine, Base
from models.movie import Movie as MovieModel

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

# create tables

Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com" and data["password"] != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credenciales invalidas")

class User(BaseModel):
    email:str
    password:str

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating:float = Field(default=10, ge=1, le=10)
    category:str = Field(default='Categoria', min_length=5, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi pelicula",
                "overview": "Descripcion de la pelicula",
                "year": 2022,
                "rating": 9.8,
                "category" : "Accion"
            }
        }

movies = [
    {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "AcciÃ³n"
	},
    {
		"id": 2,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "AcciÃ³n"
	}
]

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)

@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_movies():
    db = session
    result = db.query(MovieModel).all()
    return JSONResponse(content=result)

@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)):
    db = session
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        raise HTTPException(status_code=404, detail="No se encuentra la pelicula")
    return JSONResponse(content=result)

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    data = [ item for item in movies if item["category"] == category ]
    return JSONResponse(content=data)

@app.post('/movies', tags=['movies'], response_model=dict, status_code=status.HTTP_201_CREATED)
def create_movie(movie: Movie):
    db = session
    new_movie = MovieModel(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=movie.model_dump())

@app.put('/movies/{id}', tags=['movies'], response_model=List[Movie], status_code=status.HTTP_200_OK)
def update_movie(movie: Movie, id: int = Path(ge=1, le=2000)):
	for item in movies:
		if item["id"] == id:
			item = movie
			return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Se ha modificado la pelÃ­cula"})

@app.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=status.HTTP_200_OK)
def delete_movie(id: int = Path(ge=1, le=2000)):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Se ha eliminado la pelÃ­cula"})