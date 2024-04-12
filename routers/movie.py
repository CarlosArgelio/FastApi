from typing import List

from fastapi import APIRouter, status
from fastapi import Path, Query, Depends, HTTPException
from fastapi.responses import JSONResponse

from database.config import session
from models.movie import Movie as MovieModel
from schemas.movie import Movie as Movie
from middlewares.jwt_bearer import JWTBearer

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
    db = session
    result = db.query(MovieModel).all()
    return JSONResponse(content=result)

@movie.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)):
    db = session
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        raise HTTPException(status_code=404, detail="No se encuentra la pelicula")
    return JSONResponse(content=result)

@movie.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    data = [ item for item in movies if item["category"] == category ]
    return JSONResponse(content=data)

@movie.post('/movies', tags=['movies'], response_model=dict, status_code=status.HTTP_201_CREATED)
def create_movie(movie: Movie):
    db = session
    new_movie = MovieModel(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=movie.model_dump())

@movie.put('/movies/{id}', tags=['movies'], response_model=dict)
def update_movie(id: int, movie: Movie)-> dict:
    db = session
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message': "No encontrado"})
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
    return JSONResponse(content={"message": "Se ha modificado la pelÃ­cula"})

@movie.delete('/movies/{id}', tags=['movies'], response_model=dict, )
def delete_movie(id: int)-> dict:
    db = session
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message': "No encontrado"})
    db.delete(result)
    db.commit()
    return JSONResponse(content={"message": "Se ha eliminado la pelÃ­cula"})