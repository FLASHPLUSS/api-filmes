from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# URL base do endpoint de filmes por categoria
BASE_URL = "https://wix.maxcine.top/public/filmes"

# Dicionário para mapear as categorias e seus respectivos valores (ID do gênero)
categories = {
    "Aventura": "12",
    "Fantasia": "14",
    "Animação": "16",
    "Drama": "18",
    "Terror": "27",
    "Ação": "28",
    "Comédia": "35",
    "História": "36",
    "Faroeste": "37",
    "Thriller": "53",
    "Crime": "80",
    "Documentário": "99",
    "Ficção científica": "878",
    "Mistério": "9648",
    "Música": "10402",
    "Romance": "10749",
    "Família": "10751",
    "Guerra": "10752",
    "Cinema TV": "10770"
}

# Função para buscar filmes da categoria com base no ID da categoria
def get_movies_by_category(category_id, page=1):
    params = {'page': page, 'genre': category_id}  # Passa o ID da categoria como parâmetro
    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        return {"error": "Falha na requisição ao servidor"}, 500
    
    soup = BeautifulSoup(response.text, 'html.parser')
    movies = []
    
    for movie_div in soup.select(".info-filme"):
        title = movie_div.select_one(".titulo h1").get_text(strip=True)
        rating = movie_div.select_one(".imdb p").get_text(strip=True)
        genre = movie_div.select_one(".genres ul li strong").get_text(strip=True)
        synopsis = movie_div.select_one(".sinopse p").get_text(strip=True)
        year = movie_div.select_one(".informacoes li strong").get_text(strip=True)
        duration = movie_div.select_one(".duration li strong").get_text(strip=True)

        cover_image = movie_div.select_one(".capa img")["src"]
        banner_style = movie_div.select_one(".poster-m")["style"]
        banner_url = banner_style.split("url(")[1].split(")")[0].strip("'")

        play_url = movie_div.select_one(".play a")["href"] if movie_div.select_one(".play a") else None

        movies.append({
            "titulo": title,
            "avaliacao": rating,
            "genero": genre,
            "sinopse": synopsis,
            "ano": year,
            "duracao": duration,
            "capa": cover_image,
            "banner": banner_url,
            "play_url": play_url
        })
    
    return movies

# Rota da API para buscar filmes por categoria e página
@app.route('/api/get_by_category', methods=['GET'])
def api_get_by_category():
    category = request.args.get('category')
    page = request.args.get('page', 1)
    
    if not category:
        return jsonify({"error": "Nenhuma categoria fornecida."}), 400
    
    category_id = categories.get(category)
    
    if not category_id:
        return jsonify({"error": "Categoria inválida."}), 400
    
    movies = get_movies_by_category(category_id, page)
    return jsonify(movies)

# Rota da API para listar todas as categorias
@app.route('/api/categories', methods=['GET'])
def api_get_categories():
    return jsonify(list(categories.keys()))

# Rota da API para buscar filmes por nome
@app.route('/api/search', methods=['GET'])
def api_search_movies():
    query = request.args.get('query')
    page = request.args.get('page', 1)

    if not query:
        return jsonify({"error": "Nenhum termo de pesquisa fornecido."}), 400

    params = {'page': page, 'search': query}  # Passa o termo de pesquisa como parâmetro
    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        return {"error": "Falha na requisição ao servidor"}, 500
    
    soup = BeautifulSoup(response.text, 'html.parser')
    movies = []
    
    for movie_div in soup.select(".info-filme"):
        title = movie_div.select_one(".titulo h1").get_text(strip=True)
        rating = movie_div.select_one(".imdb p").get_text(strip=True)
        genre = movie_div.select_one(".genres ul li strong").get_text(strip=True)
        synopsis = movie_div.select_one(".sinopse p").get_text(strip=True)
        year = movie_div.select_one(".informacoes li strong").get_text(strip=True)
        duration = movie_div.select_one(".duration li strong").get_text(strip=True)

        cover_image = movie_div.select_one(".capa img")["src"]
        banner_style = movie_div.select_one(".poster-m")["style"]
        banner_url = banner_style.split("url(")[1].split(")")[0].strip("'")

        play_url = movie_div.select_one(".play a")["href"] if movie_div.select_one(".play a") else None

        movies.append({
            "titulo": title,
            "avaliacao": rating,
            "genero": genre,
            "sinopse": synopsis,
            "ano": year,
            "duracao": duration,
            "capa": cover_image,
            "banner": banner_url,
            "play_url": play_url
        })
    
    return jsonify(movies)

# Rota da API para obter todos os filmes (sem filtro de categoria ou pesquisa)
@app.route('/api/get_all_movies', methods=['GET'])
def api_get_all_movies():
    page = request.args.get('page', 1)
    response = requests.get(BASE_URL, params={'page': page})

    if response.status_code != 200:
        return {"error": "Falha na requisição ao servidor"}, 500
    
    soup = BeautifulSoup(response.text, 'html.parser')
    movies = []
    
    for movie_div in soup.select(".info-filme"):
        title = movie_div.select_one(".titulo h1").get_text(strip=True)
        rating = movie_div.select_one(".imdb p").get_text(strip=True)
        genre = movie_div.select_one(".genres ul li strong").get_text(strip=True)
        synopsis = movie_div.select_one(".sinopse p").get_text(strip=True)
        year = movie_div.select_one(".informacoes li strong").get_text(strip=True)
        duration = movie_div.select_one(".duration li strong").get_text(strip=True)

        cover_image = movie_div.select_one(".capa img")["src"]
        banner_style = movie_div.select_one(".poster-m")["style"]
        banner_url = banner_style.split("url(")[1].split(")")[0].strip("'")

        play_url = movie_div.select_one(".play a")["href"] if movie_div.select_one(".play a") else None

        movies.append({
            "titulo": title,
            "avaliacao": rating,
            "genero": genre,
            "sinopse": synopsis,
            "ano": year,
            "duracao": duration,
            "capa": cover_image,
            "banner": banner_url,
            "play_url": play_url
        })
    
    return jsonify(movies)

# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
