create table movies(
	imdb_id int,
	title varchar(255),
	title_hun varchar(255),
	males_under18_rating float,
	females_under18_rating float,
	males_18_29_rating float,
	females_18_29_rating float,
	males_30_44_rating float,
	females_30_44_rating float,
	males_over45_rating float,
	females_over45_rating float,
	constraint PK_Movie primary key (imdb_id)
);

create table actors(
	actor_id int,
	aname varchar(255),
	constraint PK_Actor primary key (actor_id)
);

create table movie_actors(
	imdb_id int,
	actor_id int,
	constraint FK_AMovie foreign key (imdb_id) references movies(imdb_id),
	constraint FK_Actor foreign key (actor_id) references actors(actor_id),
    primary key (imdb_id, actor_id)
);

create table directors(
	director_id int,
	dname varchar(255),
	constraint PK_Director primary key (director_id)
);

create table movie_directors(
	imdb_id int,
	director_id int,
	constraint FK_DMovie foreign key (imdb_id) references movies(imdb_id),
	constraint FK_Director foreign key (director_id) references directors(director_id),
    primary key (imdb_id, director_id)
);

create table genres(
	genre_id int auto_increment,
	genre varchar(255),
	constraint PK_Genre primary key (genre_id),
	constraint U_Genre unique (genre)
);

create table movie_genres(
	imdb_id int,
	genre_id int,
	constraint FK_GMovie foreign key (imdb_id) references movies(imdb_id),
	constraint FK_Genre foreign key (genre_id) references genres(genre_id),
    primary key (imdb_id, genre_id)
);

create table keywords(
	keyword_id int auto_increment,
	keyword varchar(255),
	constraint PK_Keyword primary key (keyword_id),
	constraint U_Keyword unique (keyword)
);

create table movie_keywords(
	imdb_id int,
	keyword_id int,
	constraint FK_KMovie foreign key (imdb_id) references movies(imdb_id),
	constraint FK_Keyword foreign key (keyword_id) references keywords(keyword_id),
    primary key (imdb_id, keyword_id)
);

create table users(
	user_id int,
	username varchar(255) default null,
	password varchar(255) default null,
	age int default null,
	gender boolean default null,
	constraint PK_User primary key (user_id),
    constraint U_Username unique (username)
);

create table ratings(
	imdb_id int,
	user_id int,
	rating int,
	constraint FK_RMovie foreign key (imdb_id) references movies(imdb_id),
	constraint FK_User foreign key (user_id) references users(user_id),
    primary key (imdb_id, user_id)
);