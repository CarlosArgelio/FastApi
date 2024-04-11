from fastapi import FastAPI
from fastapi import Path, Query
from fastapi.responses import HTMLResponse, JSONResponse

# schemas
from pydantic import BaseModel, Field
from typing import Optional

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

@app.get('/movies', tags=['movies'])
def get_movies():
    return JSONResponse(content=movies)

@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int = Path(ge=1, le=2000)):
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)
    # validate with error 404
    return JSONResponse(content=[])

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    data = [ item for item in movies if item["category"] == category ]
    return JSONResponse(content=data)

@app.post('/movies', tags=['movies'])
def create_movie(movie: Movie):
    movies.append(movie)
    return JSONResponse(content={"message": "Se ha registrado la pelÃ­cula"})

@app.put('/movies/{id}', tags=['movies'])
def update_movie(movie: Movie, id: int = Path(ge=1, le=2000)):
	for item in movies:
		if item["id"] == id:
			item = movie
			return JSONResponse(content={"message": "Se ha modificado la pelÃ­cula"})

@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id: int = Path(ge=1, le=2000)):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(content={"message": "Se ha eliminado la pelÃ­cula"})