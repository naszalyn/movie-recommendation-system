import DB.CRUD as CRUD

#####movie
#a visszaadott sorok tömbben/listában vannak, elemek sorrendje movies tábláéval megegyezik
def get_movie(imdb_id):
    #biztosan 1 elemet ad vissza (id miatt), de tömbbe/listába teszi, ezért kell a [0]
    return CRUD.get_movie(imdb_id)[0]

def get_movie_by_title_hun(title_hun):
    return CRUD.get_movie_by_title_hun(title_hun)

def get_movie_by_title(title):
    return CRUD.get_movie_by_title(title)

def get_all_data(imdb_id):
    m = get_movie(imdb_id)
    m_actors = get_movie_actors(imdb_id)
    m_directors = get_movie_directors(imdb_id)
    m_genres = get_movie_genres(imdb_id)
    m_keywords = get_movie_keywords(imdb_id)

    movie = []
    movie.append(m[1])
    movie.append(m[2])

    actors = []
    for i in m_actors:
        actors.append(get_actor(i[1])[1])

    directors = []
    for i in m_directors:
        directors.append(get_director(i[1])[1])

    genres = []
    for i in m_genres:
        genres.append(get_genre(i[1])[1])

    keywords = []
    for i in m_keywords:
        keywords.append(get_keyword(i[1])[1])

    all_data = {
                    'movie' : movie,
                    'actors' : actors,
                    'directors' : directors,
                    'genres' : genres,
                    'keywords' : keywords        
                }
    return all_data



#####actor
def get_movie_actors(imdb_id):
    return CRUD.get_movie_actors(imdb_id)

def get_actor(actor_id):
    return CRUD.get_actor(actor_id)[0]

#####director
def get_movie_directors(imdb_id):
    return CRUD.get_movie_directors(imdb_id)

def get_director(director_id):
    return CRUD.get_director(director_id)[0]

#####keyword
def get_movie_keywords(imdb_id):
    return CRUD.get_movie_keywords(imdb_id)

def get_keyword(keyword_id):
    return CRUD.get_keyword(keyword_id)[0]

#####genre
def get_movie_genres(imdb_id):
    return CRUD.get_movie_genres(imdb_id)

def get_genre(genre_id):
    return CRUD.get_genre(genre_id)[0]

#####user
def get_user(user_id):
    return CRUD.get_user(user_id)[0]

def get_user_by_username(username):
    user = CRUD.get_user_by_username(username)
    if len(user) > 0:    
        return user[0][0]
    else:
        return None
    
def get_user_by_sign_in_data(username, password):
    user = CRUD.get_user_by_sign_in_data(username, password)
    if len(user) > 0:    
        return user[0][0]
    else:
        return None

def insert_user(username, password, age, gender):
    CRUD.insert_user(username, password, age, gender)

def update_password(user_id, new_password):
    CRUD.update_password(user_id, new_password)


def update_username(user_id, new_username):
    same_username = CRUD.read_where('users', 'username', str(new_username))
    if len(same_username) == 0:
        CRUD.update_username(user_id, new_username)

def delete_user(user_id):
    CRUD.delete_user(user_id)

#####rating
def get_rating(user_id, imdb_id):
    rating = CRUD.get_rating(user_id, imdb_id)
    if len(rating) == 0:
        return None
    else:
        return rating[0][0]
    

def insert_rating(user_id, imdb_id, rating):
    CRUD.insert_rating(user_id, imdb_id, rating)

def update_rating(new_rating, imdb_id, user_id):
    CRUD.update_rating(new_rating, imdb_id, user_id)

def rate(user_id, imdb_id, rating):
    r = get_rating(user_id, imdb_id)
    if r is None:
        insert_rating(user_id, imdb_id, rating)
    else:
        update_rating(rating, imdb_id, user_id)

def delete_rating(imdb_id, user_id):
    CRUD.delete_rating(imdb_id, user_id)

def get_all_rating(user_id):
    return CRUD.get_all_rating(user_id)

def get_rated_movies(list):
    all = []
    for i in list:
        #0: imdb_id
        #1: user_id
        #2: rating
        movie = get_movie(i[0])
        hun_title = movie[2]
        title = movie[1]
        dict = {
                'imdb_id' : i[0],
                'hun_title' : hun_title,
                'title' : title,
                'rating' : i[2]
            }
        all.append(dict)

    return all