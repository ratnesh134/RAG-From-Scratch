from lib.search_utils import load_movies
import string

def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("","",string.punctuation))

    return text

def tokenize_text(text):
    text = clean_text(text)
    tokens = [tok for tok in text.split() if tok]
    return tokens





def search_command(query, n_results):
    movies = load_movies()
    res = []
    for movie in movies:
        
        query = clean_text(query)
        if query in clean_text(movie['title']):
            res.append(movie)
        if len(res) == n_results:
            break
    
    return res