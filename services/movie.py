from fastapi import status
from fastapi.responses import JSONResponse

from database.config import session
from models.movie import Movie
from schemas.movie import Movie as Schema

class MovieService:
    def __init__(self):
        self.db = session

    def get_movies(self):
        return self.db.query(Movie).all()

    def get_movie(self, movie_id):
        return self.db.query(Movie)\
            .filter(Movie.id == movie_id).first()

    def add_movie(self, data: Schema):
        new_movie = Movie(**data.model_dump())
        self.db.add(new_movie)
        self.db.commit()

    def update_movie(self, movie_id, data: Schema):
        result = self.db.query(Movie).filter(Movie.id == movie_id).first()
        if not result:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message': "No encontrado"})
        result.title = data.title
        result.overview = data.overview
        result.year = data.year
        result.rating = data.rating
        result.category = data.category
        self.db.commit()

    def delete_movie(self, movie_id):
        result = self.db.query(Movie).filter(Movie.id == movie_id).first()
        if not result:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message': "No encontrado"})
        self.db.delete(result)
        self.db.commit()