from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

MOVIE_URL = "https://wix.maxcine.top/public/filme/"

def get_movies_by_category(category):
    response = requests.get(f"https://wix.maxcine.top/public/categoria/{category}")
    if response.status_code != 200:
        return {"error": "Falha na requisição ao servidor"}, 500

    soup = BeautifulSoup(response.text, 'html.parser')
    movies = []

    for movie_div in soup.select(".movie-item"):
        movie_url = movie_div.select_one("a")["href"]
        movie_id = movie_url.split('/')[-1]
        img_url = movie_div.select_one("img")["src"]
        movies.append({
            "titulo": movie_id,
            "capa": img_url,
            "url": movie_url
        })

    return movies

def search_movies(query):
    response = requests.get(f"https://wix.maxcine.top/public/pesquisa?search={query}")
    if response.status_code != 200:
        return {"error": "Falha na requisição ao servidor"}, 500

    soup = BeautifulSoup(response.text, 'html.parser')
    movies = []

    for movie_div in soup.select(".suggested-item"):
        movie_url = movie_div.select_one("a")["href"]
        movie_id = movie_url.split('/')[-1]
        img_url = movie_div.select_one("img")["src"]
        movies.append({
            "titulo": movie_id,
            "capa": img_url,
            "url": movie_url
        })

    return movies

@app.route('/api/category/<category>', methods=['GET'])
def api_get_category(category):
    movies = get_movies_by_category(category)
    return jsonify(movies)

@app.route('/api/search', methods=['GET'])
def api_search():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Nenhum termo de pesquisa fornecido"}), 400
    movies = search_movies(query)
    return jsonify(movies)

def get_movie_details(movie_id):
    response = requests.get(MOVIE_URL + movie_id)
    if response.status_code != 200:
        return {"error": "Falha na requisição ao servidor"}, 500

    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.select_one(".titulo h1").get_text(strip=True) if soup.select_one(".titulo h1") else None
    rating = soup.select_one(".imdb p").get_text(strip=True) if soup.select_one(".imdb p") else None
    genre = soup.select_one(".genres ul li strong").get_text(strip=True) if soup.select_one(".genres ul li strong") else None
    synopsis = soup.select_one(".sinopse p").get_text(strip=True) if soup.select_one(".sinopse p") else None
    year = soup.select_one(".informacoes li strong").get_text(strip=True) if soup.select_one(".informacoes li strong") else None
    duration = soup.select_one(".duration li strong").get_text(strip=True) if soup.select_one(".duration li strong") else None
    banner = soup.select_one(".poster-m").get("style") if soup.select_one(".poster-m") else None
    banner_url = banner.split("url('")[1].split("')")[0] if banner else None

    movie_details = {
        "titulo": title,
        "avaliacao": rating,
        "genero": genre,
        "sinopse": synopsis,
        "ano": year,
        "duracao": duration,
        "banner": banner_url
    }

    return movie_details

@app.route('/api/movie/<movie_id>', methods=['GET'])
def api_get_movie(movie_id):
    movie_details = get_movie_details(movie_id)
    return jsonify(movie_details)

if __name__ == '__main__':
    app.run(debug=True)
