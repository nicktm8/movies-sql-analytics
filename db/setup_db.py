import db

def setup_db():
    """Setup function to check the database connection and existence of tables. 
    If the database does not exist, it will create the database and insert data."""
    
    try:
        conn = db.get_connection()
        test_query = "SELECT name FROM sqlite_master WHERE type='table' AND name='movie';"
        print(f'Testing database connection and existence of tables...')
        
        if conn.execute(test_query).fetchone() is None:
            print('Database does not exist. Creating database and inserting data...')
            db.create_tables(conn)
            db.insert_data(conn)
        else:
            print('Database already exists.')
            cursor = conn.cursor()
            
            # Verify data
            print(f"\nDatabase stats:")
            
            cursor.execute('SELECT COUNT(*) FROM movie')
            print(f"Movies: {cursor.fetchone()[0]}")
            
            cursor.execute('SELECT COUNT(*) FROM language')
            print(f"Languages: {cursor.fetchone()[0]}")
            
            cursor.execute('SELECT COUNT(*) FROM country')
            print(f"Countries: {cursor.fetchone()[0]}")
            
            cursor.execute('SELECT COUNT(*) FROM genre')
            print(f"Genres: {cursor.fetchone()[0]}")
            
            cursor.execute('SELECT COUNT(*) FROM director')
            print(f"Directors: {cursor.fetchone()[0]}")
        
    except Exception as e:
        print(f'Error connecting to the database: {e}')
    
    finally:
        try:
            conn.close()
        except Exception as e:
            print(f'Connection unavailable: {e}')

setup_db()
