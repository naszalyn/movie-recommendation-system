import DB.db_connection as db

def insert_dict(table, data):
    columns = ', '.join("`" + str(x) + "`" for x in data.keys())
    values = ', '.join("'" + replace_quote(str(x)) + "'" for x in data.values())
    sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % (table, columns, values)
    db.execute(sql)


def read_where(table, condition_column, condition_value):
    sql = "select * from %s where %s = '%s';" % (table, condition_column, replace_quote(condition_value))
    return db.read(sql)


def update_where(table, update_column, new_value, condition_column, condition_value):
    sql = "update %s set %s = '%s' where %s = '%s';" % (table, update_column, replace_quote(new_value), condition_column, replace_quote(condition_value))
    db.execute(sql)

#####user
def get_user(user_id):
    return read_where('users', 'user_id', str(user_id))

def get_user_by_sign_in_data(username, password):
    sql = "select user_id from users where username = '%s' and password = '%s';" % (replace_quote(username), replace_quote(password))
    return db.read(sql)

def get_user_by_username(username):
    return read_where('users', 'username', str(username))

def insert_user(username, password, age, gender):
    dict_user = {
                    'username' : username,
                    'password' : password,
                    'age' : age,
                    'gender' : gender        
                }
    dict_user = {k:v for k,v in dict_user.items() if v is not None}
    insert_dict('users', dict_user)


def update_password(user_id, new_password):
    update_where('users', 'password', new_password, 'user_id', str(user_id))


def update_username(user_id, new_username):
    update_where('users', 'username', new_username, 'user_id', str(user_id))

def delete_user(user_id):
    sql = "update users set username = null, password = null, age = null, gender = null where user_id = %s;" % (user_id)
    db.execute(sql)

#####rating
def get_rating(user_id, imdb_id):
    sql = "select rating from ratings where user_id = %s and imdb_id = %s;" % (user_id, imdb_id)
    return db.read(sql)

def insert_rating(user_id, imdb_id, rating):
    dict_rating = {
                        'user_id' : user_id,
                        'imdb_id' : imdb_id,
                        'rating' : rating
                  }

    insert_dict('ratings', dict_rating)

def update_rating(new_rating, imdb_id, user_id):
    sql = "update ratings set rating = %s where imdb_id = %s and user_id = %s;" % (new_rating, imdb_id, user_id)
    db.execute(sql)

def delete_rating(imdb_id, user_id):
    sql = "delete from ratings where imdb_id = %s and user_id = %s;" % (imdb_id, user_id)
    db.execute(sql)

def get_all_rating(user_id):
    return read_where('ratings', 'user_id', str(user_id))

#####movie
def get_movie(imdb_id):
    return read_where('movies', 'imdb_id', str(imdb_id))

def get_movie_by_title_hun(title_hun):
    sql = "select * from movies where title_hun like '%{}%';".format(replace_quote(title_hun))
    return db.read(sql)

def get_movie_by_title(title):
    sql = "select * from movies where title like '%{}%';".format(replace_quote(title))
    return db.read(sql)

#####movie_actors
def get_movie_actors(imdb_id):
    return read_where('movie_actors', 'imdb_id', str(imdb_id))    

#####actor
def get_actor(actor_id):
    return read_where('actors', 'actor_id', str(actor_id))

#####movie_directors
def get_movie_directors(imdb_id):
    return read_where('movie_directors', 'imdb_id', str(imdb_id))    

#####director
def get_director(director_id):
    return read_where('directors', 'director_id', str(director_id))  

#####movie_keywords
def get_movie_keywords(imdb_id):
    return read_where('movie_keywords', 'imdb_id', str(imdb_id))    

#####keyword
def get_keyword(keyword_id):
    return read_where('keywords', 'keyword_id', str(keyword_id))    

#####movie_genres
def get_movie_genres(imdb_id):
    return read_where('movie_genres', 'imdb_id', str(imdb_id))    

#####genre
def get_genre(genre_id):
    return read_where('genres', 'genre_id', str(genre_id))    



#####engine
def recommendation_by_demographic_data(demographic_group, ignore_ids):
    
    sql= """select m.imdb_id, title, title_hun from movies m
            inner join 
            (select imdb_id, count(keyword_id) k_count from movie_keywords
            group by imdb_id
            order by k_count desc
            ) k on m.imdb_id=k.imdb_id
            where 
            males_under18_rating !=0 and 
            males_18_29_rating !=0 and 
            males_30_44_rating !=0 and
            males_over45_rating !=0 and
            females_under18_rating !=0 and
            females_18_29_rating !=0 and
            females_30_44_rating !=0 and
            females_over45_rating !=0
            {}
            order by {} desc, k.k_count desc
            limit 15;
            """.format(ignore_ids, demographic_group)

    return db.read(sql)

def recommend_hybrid(id_list):
    sql = """
        select m.imdb_id, m.title, m.title_hun from movies m
        where m.imdb_id in {} order by field(m.imdb_id, {});
    """.format(tuple(id_list), ', '.join(str(x) for x in tuple(id_list)))

    return db.read(sql)


##################################
def replace_quote(text):
    return text.replace("'","''")