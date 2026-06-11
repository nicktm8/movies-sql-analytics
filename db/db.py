import sqlite3
import pandas as pd

def get_connection():
    '''Returns a connection to the SQLite database. If the database file does not exist, it will be created.'''
    
    conn = sqlite3.connect('db/movies.db')
    return conn

def create_tables(conn):
    cursor = conn.cursor()
    
    conn.execute('''
        create table if not exists movie (
            movie_id integer primary key,
            title text not null,
            release_year integer,
            duration integer,
            budget real,
            box_office real
            )
        ''')
    
    conn.execute('''
        create table if not exists language (
            language_id integer primary key,
            name text not null
            )
        ''')
    
    conn.execute('''
        create table if not exists country (
            country_id integer primary key,
            name text not null
            )
        ''')
    
    conn.execute('''
        create table if not exists genre (
            genre_id integer primary key,
            name text not null
            )
        ''')
    
    conn.execute('''
        create table if not exists director(
            director_id integer primary key,
            name text not null
            )
        ''')
    
    conn.execute('''
        create table if not exists movie_languages (
            language_id integer not null,
            movie_id integer not null,
            primary key (language_id, movie_id),
            constraint fk_language_id
            foreign key (language_id) references language (language_id)
            on update cascade on delete cascade,
            constraint fk_ml_movie_id
            foreign key (movie_id) references movie (movie_id)
            on update cascade on delete cascade
            )
            ''')
    
    conn.execute('''
        create table if not exists movie_countries (
            country_id integer not null,
            movie_id integer not null,
            primary key (country_id, movie_id),
            constraint fk_country_id
            foreign key (country_id) references country (country_id)
            on update cascade on delete cascade,
            constraint fk_mc_movie_id
            foreign key (movie_id) references movie (movie_id)
            on update cascade on delete cascade
            )
            ''')
    
    conn.execute('''
        create table if not exists movie_genres(
            genre_id integer not null,
            movie_id integer not null,
            primary key (genre_id, movie_id),
            constraint fk_genre_id
            foreign key (genre_id) references genre (genre_id)
            on update cascade on delete cascade,
            constraint fk_mg_movie_id
            foreign key (movie_id) references movie (movie_id)
            on update cascade on delete cascade
            )
            ''')
    
    conn.execute('''
        create table if not exists movie_directors (
            director_id integer not null,
            movie_id integer not null,
            primary key (director_id, movie_id),
            constraint fk_director_id
            foreign key (director_id) references director (director_id)
            on update cascade on delete cascade,
            constraint fk_md_movie_id
            foreign key (movie_id) references movie (movie_id)
            on update cascade on delete cascade
            )
            ''')
    
    conn.commit()
    
    cursor.close()

def insert_data(conn):
    df = pd.read_csv('data/movies.csv')
    
    movie_columns = ["title", "release_year", "duration", "budget", "box_office"]
    df_movie = df[movie_columns]
    df_movie.to_sql('movie', conn, if_exists='append', index=False)
     