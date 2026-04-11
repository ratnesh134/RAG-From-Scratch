from lib.search_utils import (
    load_movies,
    load_stopwords,
    CACHE_PATH,
)
import string
import os
import pickle
from nltk.stem import PorterStemmer
from collections import defaultdict, Counter

stemmer = PorterStemmer()

# For fast lookups
class InvertedIndex:

    def __init__(self):
        self.index = defaultdict(set)
        self.docmap = {} #maps document IDs: document
        self.term_frequencies = defaultdict(Counter)

        self.index_path = CACHE_PATH/'index.pkl'
        self.docmap_path = CACHE_PATH/'docmap.pkl'
        self.term_frequencies_path = CACHE_PATH/'term_frequencies.pkl'

    def __add_document(self,doc_id,text):
        tokens = tokenize_text(text)
        for token in set(tokens):
            self.index[token].add(doc_id)
        self.term_frequencies[doc_id].update(tokens)
    
    def get_documents(self,term):
        return list(self.index[term])
    
    def get_tf(self,doc_id,term):
        token = tokenize_text(term)
        if len(token) != 1:
            raise ValueError("Can only have 1 tokens")
        self.term_frequencies[doc_id][token]

    def build(self):
        movies = load_movies()
        for movie in movies:
            doc_id = movie['id']
            text = f"{movie['title']} {movie['description']}"
            self.__add_document(doc_id,text)
            self.docmap[doc_id] = movie
    
    def save(self):

        # Creating the directory,if not exist
        os.makedirs(CACHE_PATH,exist_ok=True)
        with open(self.index_path,'wb') as f:
            pickle.dump(self.index,f)
        
        with open(self.docmap_path,'wb') as f:
            pickle.dump(self.docmap,f)

        with open(self.term_frequencies_path, 'wb') as f:
            pickle.dump(self.term_frequencies,f)


    def load(self):
        with open(self.index_path,'rb') as f:
            self.index = pickle.load(f)
        
        with open(self.docmap_path,'rb') as f:
            self.docmap = pickle.load(f)
        
        with open(self.term_frequencies_path,'rb') as f:
            self.term_frequencies = pickle.load(f)


def build_command():
    idx = InvertedIndex()
    idx.build()
    idx.save()




def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("","",string.punctuation))

    return text

# Here tokenization is at word level
def tokenize_text(text):
    text = clean_text(text)
    
    # loading the stopwords
    stopwords = load_stopwords() 
    
    res = []

    # Function to remove the stopwords
    def _filter(tok):
        if tok and tok not in stopwords:
            return True
        return False
    for tok in text.split():
        if _filter(tok):

            # to get the root word
            tok = stemmer.stem(tok)
            res.append(tok)

    return res


# Function to match the tokenized words
def has_matching_token(query_tokens, movie_tokens):
    for query_tok in query_tokens:
        for movie_tok in movie_tokens:
            if query_tok in movie_tok:
                return True
            
    return False





def search_command(query, n_results):
    movies = load_movies()
    idx = InvertedIndex()
    idx.load()
    seen, res = set(), []
    query_tokens = tokenize_text(query)
    
    for qt in query_tokens:
        # use the inverted index to get any matching documentss for each token
        matching_doc_ids = idx.get_documents(qt)

        for matching_doc_id in matching_doc_ids:
            if matching_doc_id in seen:
                continue

            seen.add(matching_doc_id)
            matching_doc = idx.docmap[matching_doc_id]
            res.append(matching_doc)

            # Once we have 5 results we return the list
            if len(res) >= n_results:
                return res
            
    return res