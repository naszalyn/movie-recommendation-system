import Engine.matrices as m
from sklearn.neighbors import NearestNeighbors
import pandas as pd

#üres dataframe létrehozása, amiben a végeredmények lesznek majd
def df_empty():
    df = pd.DataFrame(columns = ["imdb_id", "score"])
    df = df.set_index("imdb_id")
    df = df.astype(float)
    return df

#df_all létrehozása, amiben benne lesznek az ajánlott filmek
df_all = df_empty()

#mátrixok és melléjük az indexek
if 'gX' not in locals():
    gX, g_imdb_mapper, g_imdb_inverse_mapper = m.genre_matrix()
    aX, a_imdb_mapper, a_imdb_inverse_mapper = m.actor_matrix()
    dX, d_imdb_mapper, d_imdb_inverse_mapper = m.director_matrix()
    kX, k_imdb_mapper, k_imdb_inverse_mapper = m.keyword_matrix()
    rX, r_imdb_mapper, r_imdb_inverse_mapper = m.rating_matrix()

#súlyok, attól függően változik majd, hogy hány filmet értékelt
class CBCFWeights:
    def __init__(self, genre_weight, actor_weight, director_weight, keyword_weight, rating_weight):
        self.genre_weight = genre_weight
        self.actor_weight = actor_weight
        self.director_weight = director_weight
        self.keyword_weight = keyword_weight
        self.rating_weight = rating_weight



def knn_algorithm(imdb_id, X, k, imdb_mapper, imdb_inverse_mapper):
    #szomszédok + távolságok lista
    neighbour_list = []
    #"belső" index megkeresése, ha használható id-t kap
    if imdb_id in imdb_mapper:
        index = imdb_mapper[imdb_id]
        #mátrix megfelelő sora vektor
        imdb_vec = X[index]
        #k értéke, minimum k szomszéd(+1 azért kell, mert általában saját magát is megtalálja)
        k += 1
        #k darab legközelebbi szomszéd megtalálása - hasonló elemek megtalálása
        kNN = NearestNeighbors(n_neighbors=k, algorithm='brute', metric='cosine', n_jobs=-1)
        kNN.fit(X)
        #visszaadja a távolságot és a belső (mátrix) indexeket
        distance, neighbour = kNN.kneighbors(imdb_vec, return_distance = True)
        for i in range(0, k):
            #a távolság értéke annál kisebb, minél hasonlóbb (közelebb van)
            #1 fölötti távolság már a legtöbb esetben vagy nagyon minimális hasonlóság,
            #       vagy random kiválasztott "szomszéd"
            #későbbi súlyozás miatt megfordítom a távolságokat, hogy akkor legyen nagyobb, amikor "közel" van
            dist = 1-distance.item(i)
            if dist > 0:
                n = neighbour.item(i)
                x = imdb_inverse_mapper[n], (dist)
                neighbour_list.append(x)    
        
    return neighbour_list

def neighbour_lists(imdb_ids):
    #megkapja az imdb id-kat, az alapján összegyűjti a g,a,d,k,r cuccokat külön listákba
    genre_neighbours = []
    actor_neighbours = []
    director_neighbours = []
    keyword_neighbours = []
    rating_neighbours = []

    for id in imdb_ids:
        genre_neighbours.extend(knn_algorithm(id, gX, 100, g_imdb_mapper, g_imdb_inverse_mapper))
        actor_neighbours.extend(knn_algorithm(id, aX, 100, a_imdb_mapper, a_imdb_inverse_mapper))
        director_neighbours.extend(knn_algorithm(id, dX, 100, d_imdb_mapper, d_imdb_inverse_mapper))
        keyword_neighbours.extend(knn_algorithm(id, kX, 100, k_imdb_mapper, k_imdb_inverse_mapper))
        rating_neighbours.extend(knn_algorithm(id, rX, 100, r_imdb_mapper, r_imdb_inverse_mapper))

    return genre_neighbours, actor_neighbours, director_neighbours, keyword_neighbours, rating_neighbours

def append_ids(neighbour_ids, weight):
    n_list = [x[0] for x in neighbour_ids]
    distances = [x[1] for x in neighbour_ids]
    index = 0
    for i in n_list:
        score = weight * distances[index]
        if i in df_all.index:
            #benne van, df-et módosítani
            df_all.loc[i]["score"] += score
        else:
            #nincs benne, hozzáadni a df-hez            
            df_all.loc[i] = score
        index += 1

def append_all_neighbours(CBCFWeights, genres, actors, directors, keywords, ratings):
    append_ids(genres, CBCFWeights.genre_weight)
    append_ids(actors, CBCFWeights.actor_weight)
    append_ids(directors, CBCFWeights.director_weight)
    append_ids(keywords, CBCFWeights.keyword_weight)
    append_ids(ratings, CBCFWeights.rating_weight)

def drop_rated_movies_from_df(rated_movies):
    for id in rated_movies:
        if id in df_all.index:
            df_all.drop(id, inplace = True)
    

def recommend_topn_movies(rated_movies, ids, n, CBCFWeights):
    global df_all
    df_all = df_empty()
    g_s, a_s, d_s, k_s, r_s = neighbour_lists(ids)
    append_all_neighbours(CBCFWeights, g_s, a_s, d_s, k_s, r_s)
    drop_rated_movies_from_df(rated_movies)
    topn = df_all.nlargest(n, "score")
    return topn.index.tolist()
    