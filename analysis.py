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
        
    print('\n2. Budget and Revenue for top 10 Movies:\n')
    print(query2_df.head(10).to_string(index=False, formatters={'budget': '${:,.2f}'.format, 'revenue': '${:,.2f}'.format}))
    print('-' * 40)
    
    print('\nAverage Budget and Revenue for All Movies:\n')
    print(movies_avg[['budget', 'revenue']].to_string())
    print('-' * 40)
    
    # Calculating Pearson correlation between budget and revenue
        
    correlation = query2_df[['budget', 'revenue']].corr().iloc[0, 1]
    print(f'\nPearson correlation between budget and revenue: {correlation:.2f}\n')
    print('=' * 40)
    
    # 3. Country Production Analysis
        
    sql_query3 = '''
    select c.name as Country, avg(m.box_office) as Revenue
    from movie m
    join movie_countries mc on mc.movie_id = m.movie_id
    join country c on c.country_id = mc.country_id
    group by Country
    order by Revenue desc
    limit 5;'''
        
    query3_df = pd.read_sql_query(sql_query3, conn)
    query3_format = query3_df.to_string(index=False, formatters={'Revenue': '${:,.2f}'.format})
        
    print('\n3. Top 5 Countries by Average Revenue:\n')
    print(query3_format)
    
    top_countries = ', '.join(query3_df['Country'].tolist())
    
    print(f'\nRecommendation: Focus on production of movies in {top_countries} due to their high average revenue.\n')
    print('=' * 40)
    
    
except Exception as e:
    print(f'Database Error: {e}')
    
finally:
    try:
        conn.close()
    except Exception as e:
        print(f'Connection unavailable: {e}')
        
try:
    plt.figure(figsize=(10, 6))
    
    query2_df['budget'] = (query2_df['budget'] / 1e6).round(2)
    query2_df['revenue'] = (query2_df['revenue'] / 1e6).round(2)
    plt.scatter(query2_df['budget'], query2_df['revenue'], alpha=0.5, color='teal', edgecolor='black')
    
    plt.title(f'Relationship between Budget and Revenue (Correlation: {correlation:.2f})', fontsize=14, fontweight='bold')
    plt.xlabel('Movie Budget (Millions $)', fontsize=12)
    plt.ylabel('Box Office Revenue (Millions $)', fontsize=12)
    
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    
    plt.savefig('output/budget_revenue_scatter_plot.png')
    #plt.show()
    

except NameError:
    print('Data not available for scatter plot visualisation.')
