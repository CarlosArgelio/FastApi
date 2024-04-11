from fastapi import FastAPI
from fastapi.responses import HTMLResponse

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
    return movies

@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int):
    for item in movies:
        if item["id"] == id:
            return item
    # validate with error 404
    return []

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str, year: int):
    return category