import sqlite3
import pandas as pd

def get_connection():
    '''Returns a connection to the SQLite database. If the database file does not exist, it will be created.'''
    
    conn = sqlite3.connect('db/movies.db')
    conn.execute('PRAGMA foreign_keys = ON')
    
    print('Connection established to SQLite database.')
        
    return conn

def create_tables(conn):
    cursor = conn.cursor()
    
    print('Creating tables if they do not exist...')
        
    conn.execute('''
        create table if not exists movie (
            movie_id integer primary key,
            title text unique not null,
            release_year integer,
            duration integer,
            budget real,
            box_office real
            )
        ''')
    
    conn.execute('''
        create table if not exists language (
            language_id integer primary key,
            name text unique not null
            )
        ''')
    
    conn.execute('''
        create table if not exists country (
            country_id integer primary key,
            name text unique not null
            )
        ''')
    
    conn.execute('''
        create table if not exists genre (
            genre_id integer primary key,
            name text unique not null
            )
        ''')
    
    conn.execute('''
        create table if not exists director(
            director_id integer primary key,
            name text unique not null
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
    
    print('Tables created successfully.')

def insert_data(conn):
    df = pd.read_csv('data/movies.csv')
    
    print(f'✓ Loaded CSV with: {df.shape[0]} rows and {df.shape[1]} columns.')
        
    movie_columns = ['title', 'release_year', 'duration', 'budget', 'box_office']
    df_movie = df[movie_columns].drop_duplicates(subset=['title', 'release_year'])
    df_movie.to_sql('movie', conn, if_exists='append', index=False)
    
    print(f'Inserted {len(df_movie)} unique movies into movie table.')
        
    for i, row in df.iterrows():
        movie_id = conn.execute('select movie_id from movie where title = ? and release_year = ?', (row['title'], row['release_year'])).fetchone()[0]
        
        if pd.notna(row['language']):
            languages = [l.strip() for l in row['language'].split(',')]
            for language in languages:
                conn.execute('INSERT OR IGNORE INTO language (name) VALUES (?)', (language,))
                language_id = conn.execute('SELECT language_id FROM language WHERE name = ?', (language,)).fetchone()[0]
                conn.execute('INSERT OR IGNORE INTO movie_languages VALUES (?, ?)', (language_id, movie_id))
        
        if pd.notna(row['country']):
            countries = [c.strip() for c in row['country'].split(',')]
            for country in countries:
                conn.execute('INSERT OR IGNORE INTO country (name) VALUES (?)', (country,))
                country_id = conn.execute('SELECT country_id FROM country WHERE name = ?', (country,)).fetchone()[0]
                conn.execute('INSERT OR IGNORE INTO movie_countries VALUES (?, ?)', (country_id, movie_id))
        
        if pd.notna(row['genre']):
            genres = [g.strip() for g in row['genre'].split(',')]
            for genre in genres:
                conn.execute('INSERT OR IGNORE INTO genre (name) VALUES (?)', (genre,))
                genre_id = conn.execute('SELECT genre_id FROM genre WHERE name = ?', (genre,)).fetchone()[0]
                conn.execute('INSERT OR IGNORE INTO movie_genres VALUES (?, ?)', (genre_id, movie_id))
        
        if pd.notna(row['director']):
            directors = [d.strip() for d in row['director'].split(',')]
            for director in directors:
                conn.execute('INSERT OR IGNORE INTO director (name) VALUES (?)', (director,))
                director_id = conn.execute('SELECT director_id FROM director WHERE name = ?', (director,)).fetchone()[0]
                conn.execute('INSERT OR IGNORE INTO movie_directors VALUES (?, ?)', (director_id, movie_id))
        
    conn.commit()
    
    print(f'Inserted data for {len(df)} movies into language, country, genre, and director tables.')

def main():
    try:
        conn = get_connection()
        create_tables(conn)
        insert_data(conn)
        
    except Exception as e:
        print(f'Error: {e}')
    
    finally:
        conn.close()

main()