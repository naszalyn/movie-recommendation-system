"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from WebRequests import web_requests as wr
from Engine import recommendation as rec
from flask import Flask, render_template, redirect, request, url_for, session
app = Flask(__name__)
app.secret_key = 'rnd'

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/')
def hello():
    """Renders a sample page."""
    return render_template('sign_in.html')

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/sign_out')
def sign_out():
    session.pop('user_id', None)
    return redirect('/')

@app.route('/check_data', methods = ['GET', 'POST'])
def check_data():
    #a felhasználónév+jelszó ellenőrzése
    #visszairányít a /-re
    #vagy betölti a kezdőoldalt 
    username = request.form['username']
    pw = request.form['password']
    user = wr.get_user_by_sign_in_data(username, pw)
    if user is not None:
        session['user_id'] = user
        return redirect(url_for('main_page'))
        #bejelentkezés, megvan a userid
        #átirányít a főoldalra
    else:
        return redirect('/')
        #visszairányítás
 
@app.route('/check_sign_up_data', methods = ['GET', 'POST'])
def sign_up_data():
    username = request.form['username']
    pw = request.form['password']
    age = request.form['age']
    gender = request.form['gender']
    #van-e már ilyen user
    user = wr.get_user_by_username(username)
    if user is None:
        wr.insert_user(username, pw, age, gender)
    else:
        #van -> újratölti a regisztrációs formot
        return redirect('/sign_up')
    user = wr.get_user_by_sign_in_data(username, pw)
    if user is None:
        return redirect('/sign_up')
    else:
        user_id = wr.get_user_by_username(username)
        session['user_id'] = user_id
        return redirect('/main_page')

@app.route('/check_update_username', methods = ['GET', 'POST'])
def check_update_username():
    username = request.form['username']
    #van-e már ilyen user
    user = wr.get_user_by_username(username)
    if user is None:
        wr.update_username(session['user_id'], username)
    return redirect('/user_profile')
        
@app.route('/update_password', methods = ['GET', 'POST'])
def update_password():
    wr.update_password(session['user_id'], request.form['password'])
    return redirect('/user_profile')

@app.route('/delete_account')
def delete_account():
    wr.delete_user(session['user_id'])
    return redirect('/')

@app.route('/main_page', methods = ['GET', 'POST'])
def main_page():
    #megjeleníteni username-et
    user_id = session['user_id']
    user = wr.get_user(user_id)
    return render_template('main_page.html', user = user)

@app.route('/search_list', methods = ['GET', 'POST'])
def search_list():
    title_hun = request.form['text']
    movies = wr.get_movie_by_title_hun(title_hun)
    return render_template('movie_list.html', data = movies)

@app.route('/search_list_original_title', methods = ['GET', 'POST'])
def search_list_original_title():
    title = request.form["original_title"]
    movies = wr.get_movie_by_title(title)
    return render_template('movie_list.html', data = movies)

@app.route('/movie_page/<imdb_id>', methods = ['GET', 'POST'])
def get_movie(imdb_id):
    all_data = wr.get_all_data(imdb_id)
    movie = all_data['movie']
    actors = all_data['actors']
    directors = all_data['directors']
    genres = all_data['genres']
    keywords = all_data['keywords']
    user_id = session['user_id']
    rating = wr.get_rating(user_id, imdb_id)
    #minden adata a filmnek, megjeleníteni az oldalon
    return render_template('movie_page.html', rating = rating, imdb_id = imdb_id, movie = movie, actors=actors, directors=directors, genres=genres, keywords=keywords)

@app.route('/recommendations')
def get_recommendations():
    user_id = session['user_id']
    rec_movies = rec.recommend(user_id)
    return render_template('movie_list.html', data = rec_movies)

@app.route('/rate/<imdb_id>', methods = ['GET', 'POST'])
def rate(imdb_id):
    user_id = session['user_id']
    rating = request.form['rating']
    wr.rate(user_id, imdb_id, rating)
    return redirect('/movie_page/{}'.format(imdb_id))

@app.route('/rated_movies')
def rated_movies():
    ratings = wr.get_all_rating(session['user_id'])
    data = wr.get_rated_movies(ratings)
    return render_template('rated_movies.html', data = data)

@app.route('/delete_rating/<imdb_id>', methods = ['GET', 'POST'])
def delete_rating(imdb_id):
    user_id = session['user_id']
    wr.delete_rating(imdb_id, user_id)
    return redirect('/movie_page/{}'.format(imdb_id))

@app.route('/user_profile')
def user_profile():
    user = wr.get_user(session['user_id'])
    return render_template('user_profile.html', user = user)

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)

