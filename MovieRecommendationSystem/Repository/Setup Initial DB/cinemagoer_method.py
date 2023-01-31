from imdb import Cinemagoer

ia = Cinemagoer()


#minden adat
def get_all(id):
   all = ia.get_movie_main(id)
   return all
    


def get_data_movies_table(all, id):
    #originial title
    original_title = ""
    if 'original title' in all['data']:
        original_title = all['data']['original title']

    #Hungarian title
    all_titles = ia.get_movie_akas(id)
    hun_title = ""       
    if 'raw akas' in all_titles['data']:
        titles = all_titles['data']['raw akas']
        for i in titles:
            if 'countries' in i and i['countries'] == 'Hungary':
                hun_title = i['title']
                break
            
    #votes
    votes = ia.get_movie_vote_details(id)

    groups = ['ttrt fltr males aged under 18', 'ttrt fltr males aged 18 29',
      'ttrt fltr males aged 30 44', 'ttrt fltr males aged 45 plus',
      'ttrt fltr females aged under 18','ttrt fltr females aged 18 29',
      'ttrt fltr females aged 30 44','ttrt fltr females aged 45 plus']

    dvotes = []
    if 'demographics' in votes['data']:
        for i in groups:    
            if i in votes['data']['demographics']:
                x = votes['data']['demographics'][i]['rating']
                dvotes.append(x)
            else:
                dvotes.append(0)
    else:
        dvotes = [0, 0, 0, 0, 0, 0, 0, 0]

    dictmovie = {
       "imdb_id" : id,
       "title" : original_title,
       "title_hun" : hun_title,
       "males_under18_rating":dvotes[0],
       "males_18_29_rating":dvotes[1],
       "males_30_44_rating":dvotes[2],
       "males_over45_rating":dvotes[3],
       "females_under18_rating":dvotes[4],
       "females_18_29_rating":dvotes[5],
       "females_30_44_rating":dvotes[6],
       "females_over45_rating":dvotes[7]
        }

    return dictmovie
    

def get_data_actors_table(all):
    #cast
    cast = []
    if 'cast' in all['data']:
        cast = all['data']['cast']
    
    actors = []
    for i in cast:
        x = {
                'actor_id' : i.personID,
                'aname' : i.data['name']
            }        
        actors.append(x)

    return actors

def get_data_directors_table(all):
    #director
    all_directors = []
    if 'director' in all['data']:
        all_directors = all['data']['director']
    
    directors = []
    for i in all_directors:
        x = {
                'director_id' : i.personID,
                'dname' : i.data['name']
            }  
        directors.append(x)

    return directors

def get_data_keywords_table(id):
        #keywords
        keywordsAll = ia.get_movie_keywords(id)
        #relevant keywords, total_votes, votes_for:
        #hányan találták megfelelőnek a kulcsszavakat, csak azokat kell
        #figyelembe venni,
        #    ahol ...  az arány
        keywordsRelevant = []
        keywords = []
        if 'relevant keywords' in keywordsAll['data']:
            for i in keywordsAll['data']['relevant keywords']:
                if 'total_votes' in i and 'votes_for' in i:
                    if int(i['total_votes']) >= 3 and int(i['votes_for']) / int(i['total_votes']) > 0.8:
                        keywordsRelevant.append(i)            
            
            for i in keywordsRelevant:
                 x = {
                         'keyword' : i['keyword']
                     }  
                 keywords.append(x)

        return keywords
    
def get_data_genres_table(all):
    
    genres = []
    if 'genres' in all['data']:
        genrelist = all['data']['genres']
        for i in genrelist:
            x = {
                    'genre' : i
                }
            genres.append(x)

    return genres