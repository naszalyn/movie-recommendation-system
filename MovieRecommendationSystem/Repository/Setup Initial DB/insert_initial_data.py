import pandas as pd
import cinemagoer_method as cm
import DB.CRUD as CRUD
import DB.db_connection as db
import time


#meghívja a listaelemekre a cinemagoer metódust
#kéri egy másik résztől a beszúrást a táblába



def initial_db_data(num):

  file_to_read = 'imdb_ids_{}.csv'.format(num)
  error_file = 'errors_{}.txt'.format(num)

  ids = pd.read_csv(file_to_read, header=None)

  id_list = []
  for i in ids[0]:
      x = "{:>07}".format(str(i))
      id_list.append(x)  
  
  for id in id_list:
    #megkapja az adatokat
    try:
        all = cm.get_all(id)
        
        time.sleep(1)

        data = cm.get_data_movies_table(all, id)
        #beilleszti a táblákba
        CRUD.insert_dict('movies', data)
        
        actor_data = cm.get_data_actors_table(all)
        for a in actor_data:
            CRUD.insert_dict('actors', a)
            #   +kapcsolótábla
            rel_data = {
                            'imdb_id' : id,
                            'actor_id' : a['actor_id']
                       }
            CRUD.insert_dict('movie_actors', rel_data)

        director_data = cm.get_data_directors_table(all)
        for d in director_data:
            CRUD.insert_dict('directors', d)
            
            rel_data = {
                            'imdb_id' : id,
                            'director_id' : d['director_id']
                       }
            CRUD.insert_dict('movie_directors', rel_data)
        
        time.sleep(1)

        keyword_data = cm.get_data_keywords_table(id)
        for k in keyword_data:
            CRUD.insert_dict('keywords', k)
            ####### read-del megkeresi a kapott id-t
            kw = CRUD.read_where('keywords', 'keyword', k['keyword'])
            rel_data = {
                            'imdb_id' : id,
                            'keyword_id' : kw[0][0]
                       }
            CRUD.insert_dict('movie_keywords', rel_data)       

        genre_data = cm.get_data_genres_table(all)
        for g in genre_data:
            CRUD.insert_dict('genres', g)
            ####### read-del megkeresi a kapott id-t
            gr = CRUD.read_where('genres', 'genre', g['genre'])
            rel_data = {
                            'imdb_id' : id,
                            'genre_id' : gr[0][0]
                       }
            CRUD.insert_dict('movie_genres', rel_data)
        
    except:
        with open(error_file, "a") as myfile:
            text = id + "\n"
            myfile.write(text)


  db.close_connection()



#initial_db_data(12)