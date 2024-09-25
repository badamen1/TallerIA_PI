import os
import json
import numpy as np
from dotenv import load_dotenv
from django.shortcuts import render
from openai import OpenAI
from movie.models import Movie
from django.http import JsonResponse

_ = load_dotenv('../api_keys.env')
client = OpenAI(api_key=os.environ.get('openai_apikey'))

with open('../movie_descriptions_embeddings.json', 'r') as file:
    movies_embeddings = json.load(file)

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def recommend_movie(request):
    search_term = request.GET.get('searchMovie', '')
    if search_term:
        query = search_term
        emb = get_embedding(query)
        sim = []
        for movie in movies_embeddings:
            sim.append(cosine_similarity(emb, movie['embedding']))
        idxsort = np.argsort(sim)[::-1]
        recommended_titles = [movies_embeddings[i]['title'] for i in idxsort[:10]]
        recommended_movies = Movie.objects.filter(title__in=recommended_titles)
        return render(request, 'index.html', {'searchTerm': search_term, 'movies': recommended_movies})
    return render(request, 'index.html', {'searchTerm': search_term, 'movies': []})
