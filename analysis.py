import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import db.database as db


try:
    conn = db.setup_db()

    # 1. Genre Analysis and Investment Recommendations

    sql_query = '''
    select g.name as Genre, sum(m.box_office) as Revenue
    from movie m
    join movie_genres mg on mg.movie_id = m.movie_id
    join genre g on g.genre_id = mg.genre_id
    group by g.name
    order by Revenue desc
    limit 3;'''

    query_df = pd.read_sql(sql_query, conn)

    print('=' * 40)
    print('\n1. Top 3 Genres by Revenue:\n')
    print(query_df.to_string(index=False, formatters={'Revenue': '${:,.2f}'.format}))
    
    top_genres = ', '.join(query_df['Genre'].tolist())
    print(f'\nRecommendation: Focus on {top_genres} due to their high revenue.\n')
    
except Exception as e:
    print(f'Database Error: {e}')
    
finally:
    try:
        conn.close()
    except Exception as e:
        print(f'Connection unavailable: {e}')
