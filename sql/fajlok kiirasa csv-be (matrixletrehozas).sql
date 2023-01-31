/*A movie_keywords, movie_genres, movie_actors, movie_directors táblákra lefuttatva.
A ratings tábla adatai az értékelésekkel megvannak az átalakított fájlban, az használható a mátrixhoz is.
(Elegendő átnevezni, hogy az alkalmazás felismerje a fájlt: movie_ratings.)*/
select *, 1 from movie_keywords
INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/movie_keywords.csv' 
FIELDS ENCLOSED BY '' 
TERMINATED BY ','
LINES TERMINATED BY '\r\n';