from db import get_connection

def test():
    try:
        conn = get_connection()
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
        print(f'Error: {e}')
    
    finally:
        conn.close()

test()
