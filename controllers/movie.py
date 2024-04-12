from services.movie import MovieService

class MovieController:
    def __init__(self, services = MovieService):
        self.movie_service = services

    def get_movies(self):
        return self.movie_service.get_movies()

    def get_movie(self, movie_id):
        return self.movie_service.get_movie(movie_id)

    def add_movie(self, data):
        return self.movie_service.add_movie(data)

    def update_movie(self, movie_id, data):
        return self.movie_service.update_movie(movie_id, data)

    def delete_movie(self, movie_id):
        return self.movie_service.delete_movie(movie_id)