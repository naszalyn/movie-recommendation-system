import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
######create matrix
def create_matrix(table):
    csv = 'movie_{}.csv'.format(table)
    df = pd.read_csv(csv, header = None)

    #mekkora legyen a mátrix (NxM)
    N = len(df.iloc[:,0].unique())
    M = len(df.iloc[:,1].unique())
      
    #mindegyik i-hez hozzárendel egy indexet
    imdb_mapper = {k: v for k, v in zip(np.unique(df.iloc[:,0]), list(range(N)))}
    table_mapper = {k: v for k, v in zip(np.unique(df.iloc[:,1]), list(range(M)))}

    #visszafelé/inverz, hogy könnyebb legyen megtalálni a belső index alapján az eredetit
    imdb_inverse_mapper = {k: v for k, v in zip(list(range(N)), np.unique(df.iloc[:,0]))}

    #dataframe alapján "átváltja" az eredeti indexeket az előbb generáltakra
    imdb_index = [imdb_mapper[i] for i in df.iloc[:,0]]
    table_index = [table_mapper[i] for i in df.iloc[:,1]]

    #mátrix felépítése, NxM-es, generált indexeket és a dataframe 3. oszlopát használva épül fel
    X = csr_matrix((df.iloc[:,2], (imdb_index, table_index)), shape=(N, M))

    return X, imdb_mapper, imdb_inverse_mapper

def genre_matrix():
    return create_matrix('genres')

def actor_matrix():
    return create_matrix('actors')

def director_matrix():
    return create_matrix('directors')

def keyword_matrix():
    return create_matrix('keywords')

def rating_matrix():
    return create_matrix('ratings')