from lib.search_utils import load_movies

def search_command(query, n_results):
    movies = load_movies()

    for movie in movies:
        res = []
        if query in movies['title']:
            res.append(movie)
        if len(res) == n_results:
            break
    
    return res