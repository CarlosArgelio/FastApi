from typing import List

from fastapi import APIRouter, status
from fastapi import Path, Query, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from schemas.movie import Movie as Movie
from middlewares.jwt_bearer import JWTBearer
from controllers.movie import MovieController

movie = APIRouter()

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

@movie.get('/movies', tags=['movies'], response_model=List[Movie], status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_movies():
    controller = MovieController()
    result = controller.get_movies()
    return JSONResponse(content=jsonable_encoder(result))

@movie.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)):
    controller = MovieController()
    result = controller.get_movie(id)
    if not result:
        raise HTTPException(status_code=404, detail="No se encuentra la pelicula")
    return JSONResponse(content=jsonable_encoder(result))

@movie.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    data = [ item for item in movies if item["category"] == category ]
    return JSONResponse(content=data)

@movie.post('/movies', tags=['movies'], response_model=dict, status_code=status.HTTP_201_CREATED)
def create_movie(movie: Movie):
    controller = MovieController()
    controller.add_movie(movie)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=movie.model_dump())

@movie.put('/movies/{id}', tags=['movies'], response_model=dict)
def update_movie(id: int, movie: Movie)-> dict:
    controller = MovieController()
    controller.update_movie(id, movie)
    return JSONResponse(content={"message": "Se ha modificado la pelÃ­cula"})

@movie.delete('/movies/{id}', tags=['movies'], response_model=dict, )
def delete_movie(id: int)-> dict:
    controller = MovieController()
    controller.delete_movie(id)
    return JSONResponse(content={"message": "Se ha eliminado la pelÃ­cula"})