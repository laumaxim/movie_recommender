import random
import pandas as pd
import numpy as np
from json import dump
from sklearn.impute import KNNImputer
from sklearn.decomposition import NMF
from sklearn.metrics.pairwise import cosine_similarity
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static')
movies = pd.read_csv(os.path.join(APP_STATIC,'movies.csv'))

#movies = pd.concat([movies,movies['genres'].str.get_dummies()],axis=1)
#movies_json = movies[['movieId','title','genres']].to_json('movies.json',orient='records')

ratings = pd.read_csv(os.path.join(APP_STATIC,'ratings.csv'))

top_ratings = ratings.groupby('movieId')['rating'].agg(['mean','count']).sort_values(['mean','count'],ascending=False)

THRESHOLD = 15
top = ratings.groupby('movieId')['rating'].agg(['mean','count']).sort_values(['mean','count'],ascending=False)
top = top[top['count'] > THRESHOLD]

reviews = pd.pivot_table(
            ratings,values='rating',
            index='userId',
            columns='movieId')
#imputer = KNNImputer(n_neighbors=5, weights='distance')
#reviews = pd.DataFrame(
#        imputer.fit_transform(reviews),
 #       columns=reviews.columns,
  #      index=reviews.index)

#nmf = NMF(n_components=20)
#rhat = nmf.fit_transform(reviews)

def get_top_predict(user_dict,k=10):
    seen = list(user_dict.keys())
    ids = top[~top.index.isin(seen)].head(k).index.tolist()
    return movieId_to_title(ids)


def add_user_to_reviews(user_dict,reviews):
    ''' Adds a new user to the reviews DataFrame
    Arguments:
    user_dict -- dictionary of movie ratings for the user in the form
                {movieId: rating}, where rating is 0.5 ... 5.0 in steps of 0.5
    reviews   -- DataFrame with columns 'movieId' and rows userId
    
    returns   -- DataFrame with added row of the new user rating
    '''
    user_series = pd.Series(
        data=user_dict,
        name=reviews.index.max()+1,
        dtype=float)
    return reviews.append(user_series)


def cos_similar(reviews):
    '''Given a DataFram of users and movie reviews, returns a DataFrame with the cosine similarity of each user.
    '''
    reviews = reviews.fillna(0.0)
    sim = cosine_similarity(reviews)
    user_similar = pd.DataFrame(sim,index=reviews.index,columns=reviews.index)
    return user_similar


def get_top_of_user(reviews,user_id,k=20):
    '''Returns a list of the k top-rated moviesIds of a given user'''
    #order = np.argsort(reviews.loc[user_id])[::-1]
    user_reviews = reviews.loc[user_id]
    top_rated = user_reviews.sort_values(ascending=False)
    return top_rated.index.tolist()[:k]


def get_similar_users(user_id,similar_matrix,k=20):
    ''' Returns a list of similar users.

    Arguments:
    user_id        -- id of user that the other users are compared to
    similar_matrix -- DataFram of user similarity, must contain user_id
    k              -- number of similar users returned. (Default=20)
    '''
    #cosim = cos_similar(similar_matrix)
    user = similar_matrix.loc[[user_id]]
    user = user.drop(user_id,axis=1)
    sort = np.argsort(user.values.flatten())
    print(len(sort))
    most_similar = user.columns[sort[::-1]].tolist()
    return most_similar[:k]


def recommend(user_id, top_list, ratings, k):
    '''Recommends a movie that the user_id has not been rated in the ratings dataframe. The best k recommendations from the top_list dataframe are returned as a list. '''
    seen = list(ratings[ratings.userId==user_id]['movieId'])
    return top_list[~top_list.index.isin(seen)].head(k).index.tolist()


def movieId_to_title(ids):
    ''' Given a list of movieIds, returns a corresponding list of movie titles.
    '''
    return movies.set_index('movieId').loc[ids]['title'].tolist()

def title_to_movieId(titles):
    ''' Given a list of movie titles, returns a corresponding list of movieIds.
    '''
    return movies.set_index('title').loc[titles]['movieId'].tolist()
    

def matrix_factor():
    return ''

def cosim_predict(dict_of_ratings):
    '''
    Gives a prediction of movies to see, based on reviews of movies given.
    '''
    seen = set(dict_of_ratings.keys())
    reviews_added  = add_user_to_reviews(dict_of_ratings,reviews)
    similar_matrix = cos_similar(reviews_added)
    similar_users  = get_similar_users(reviews_added.shape[0],similar_matrix,1)
    movieIds       = get_top_of_user(reviews, similar_users[0])
    return movieId_to_title([item for item in movieIds if item not in seen])

