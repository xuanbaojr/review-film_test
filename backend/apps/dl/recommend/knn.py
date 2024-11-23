import pandas as pd
import numpy as np
import json
import os

import operator
from scipy import spatial

current_dir = os.path.dirname(__file__)

class KNN():
    def __init__(self, train_dir="movies.csv") -> None:
        self.movies = pd.read_csv(os.path.join(current_dir, train_dir))

    def compute_similarity(self, id1, id2):
        
        movie_1, movie_2 = self.movies.iloc[id1], self.movies.iloc[id2]

        genre_1, genre_2 = movie_1['genres_bi'], movie_2['genres_bi']
        genre_1 = [int(x) for x in genre_1.strip("[]").replace(" ","").split(",")]
        genre_2 = [int(x) for x in genre_2.strip("[]").replace(" ","").split(",")]

        cast_1, cast_2 = movie_1['cast_bi'], movie_2['cast_bi']
        cast_1 = [int(x) for x in cast_1.strip("[]").replace(" ","").split(",")]
        cast_2 = [int(x) for x in cast_2.strip("[]").replace(" ","").split(",")]

        director_1, director_2 = movie_1['director_bi'], movie_2['director_bi']
        director_1 = [int(x) for x in director_1.strip("[]").replace(" ","").split(",")]
        director_2 = [int(x) for x in director_2.strip("[]").replace(" ","").split(",")]

        keywords_1, keywords_2 = movie_1['keywords_bi'], movie_2['keywords_bi']
        keywords_1 = [int(x) for x in keywords_1.strip("[]").replace(" ","").split(",")]
        keywords_2 = [int(x) for x in keywords_2.strip("[]").replace(" ","").split(",")]

        genre_distance = spatial.distance.cosine(genre_1, genre_2)
        cast_distance = spatial.distance.cosine(cast_1, cast_2)
        director_distance = spatial.distance.cosine(director_1, director_2)
        keywords_distance = spatial.distance.cosine(keywords_1, keywords_2)

        return genre_distance + cast_distance + 0.5*director_distance + keywords_distance 
        
    def predict(self, input_data):
        k = 5
        target_film = self.movies[self.movies['original_title'] == input_data]

        distances = []
        for index, row in self.movies.iterrows():
            if row['new_id'] != target_film["new_id"].to_list()[0]:
                distance = self.compute_similarity(row['new_id'], target_film['new_id'].to_list()[0])
                distances.append((row,distance))

        results = []
        distances.sort(key=operator.itemgetter(1))
        for i in range(k):
            neighbors = distances[i][0]
            results.append(neighbors['original_title'])
        
        return results