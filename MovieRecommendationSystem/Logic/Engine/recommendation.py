import DB.CRUD as CRUD
import Engine.algorithm as alg

def recommend_demographic(is_male, age, rated_movies):
    if age < 18:
        category = "under18"
    elif age < 30:
        category = "18_29"
    elif age < 45:
        category = "30_44"
    else:
        category = "over45"

    if is_male:
        demographic_group = "males_{}_rating".format(category)
    else:
        demographic_group = "females_{}_rating".format(category)

    ignore_ids = ""
    if len(rated_movies) > 0:
        ignore_ids = "and m.imdb_id not in (" + ', '.join(str(x) for x in tuple(rated_movies)) + ")"

    return CRUD.recommendation_by_demographic_data(demographic_group, ignore_ids)

def recommend_hybrid(rated_movies, favourite_movies, topn, weights):
    topn_movies = alg.recommend_topn_movies(rated_movies, favourite_movies, topn, weights)
    return CRUD.recommend_hybrid(topn_movies)

def get_favourite_movies(rated_movies):
    #azok a filmek, amiket jóra értékelt
    #átlagos értékelése feletti értékelésű filmek
    favourite_movies = []
    sum = 0
    count = len(rated_movies)
    for i in rated_movies:
        sum += i[2]
    avg = sum / count
    for i in rated_movies:
        if i[2] >= avg:
            favourite_movies.append(i[0])
    return favourite_movies

def recommend(user_id):
    rated_movies = CRUD.get_all_rating(user_id)
    #értékelt filmek id-ja
    rated_movies_list = []
    for i in rated_movies:
        rated_movies_list.append(i[0])
    if len(rated_movies) < 5:
        user = CRUD.get_user(user_id)[0]
        return recommend_demographic(user[4], user[3], rated_movies_list)
    else:
        #saját átlagnál jobbra értékelt filmek
        ids = get_favourite_movies(rated_movies)
        #ha max 10 filmet értékelt, akkor jobban hagyatkozik a CB-re (tartalomalapú)
        if len(rated_movies) < 10:
            weights = alg.CBCFWeights(0.1125, 0.225, 0.15, 0.2625, 0.25)
        #ha 10+ filmet értékelt, akkor CF (más felhasználók értékelései) jobban számít
        else:
            weights = alg.CBCFWeights(0.09, 0.18, 0.12, 0.21, 0.4)
        return recommend_hybrid(rated_movies_list, ids, 15, weights)
    


