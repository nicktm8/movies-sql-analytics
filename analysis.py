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
    print('=' * 40)
    
    # 2. Budget and Revenue Relationship
        
    sql_query2 = 'select title, budget, box_office as revenue from movie'
        
    query2_df = pd.read_sql_query(sql_query2, conn)
    query2_df['revenue']  = pd.to_numeric(query2_df['revenue'], errors='coerce')
    movies_avg = query2_df.mean(numeric_only=True).apply(lambda x: f'${x:,.2f}')
        
    print('\nBudget and Revenue for top 10 Movies:\n')
    print(query2_df.head(10).to_string(index=False, formatters={'budget': '${:,.2f}'.format, 'revenue': '${:,.2f}'.format}))
        
    print('\nAverage Budget and Revenue for All Movies:\n')
    print(movies_avg[['budget', 'revenue']].to_string())
    print('=' * 40)
    
    # Calculating Pearson correlation between budget and revenue
        
    correlation = query2_df[['budget', 'revenue']].corr().iloc[0, 1]
    print(f'\nPearson correlation between budget and revenue: {correlation:.2f}\n')
    print('=' * 40)
    
except Exception as e:
    print(f'Database Error: {e}')
    
finally:
    try:
        conn.close()
    except Exception as e:
        print(f'Connection unavailable: {e}')
