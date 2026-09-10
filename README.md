# 🎬 Movies SQL Analytics

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.0+-11557c?style=flat&logo=python&logoColor=white)](https://matplotlib.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-0.12+-4C72B0?style=flat&logo=python&logoColor=white)](https://seaborn.pydata.org/)
[![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat)](https://github.com/nicktm8/movies-sql-analytics)

A SQL analytics project that explores financial and production trends across 543 films. Data is loaded into a normalized SQLite database and queried using SQL and Python (pandas, Matplotlib, Seaborn) to surface insights on genre profitability, budget-revenue correlation, and country production trends.

---

## ⚙️ Features

- Loads a raw CSV dataset into a normalized 9-table SQLite schema
- Identifies the top 3 most profitable genres by total revenue
- Analyzes the relationship between budget and box office revenue (Pearson correlation)
- Ranks the top 5 countries by average revenue per film
- Lists the top 10 highest-grossing films
- Generates and saves scatter plot and bar chart visualizations
- Auto-initializes the database on first run — no manual setup required

---

## 🏗️ Project Structure

```
movies-sql-analytics/
│
├── data/
│   └── movies.csv              # Source dataset (543 films)
│
├── db/
│   ├── database.py             # get_connection(), create_tables(), insert_data(), setup_db()
│   └── schema.sql              # DDL reference (CREATE TABLE statements)
│
├── output/
│   ├── budget_revenue_scatter_plot.png     # Budget vs. revenue (generated)
│   └── top_countries_avg_revenue_bar_plot.png  # Top 5 countries (generated)
│
├── analysis.py                 # SQL queries + pandas analysis + visualizations
├── requirements.txt
├── .gitignore                  # Excludes movies.db and output/
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher

### Installation

1. Clone the repository:

```
git clone https://github.com/nicktm8/movies-sql-analytics.git
cd movies-sql-analytics
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run the analysis:

```
python analysis.py
```

The database is created and populated automatically on first run.

---

## 📊 Analysis Overview

### 1. Genre Analysis

Identifies the top 3 genres by total box office revenue using `GROUP BY`, `SUM()`, and `JOIN` across the normalized schema.

```
Top 3 Genres by Revenue:
    Genre            Revenue
Adventure $48,032,754,962.00
   Action $44,415,784,486.00
    Drama $36,064,596,188.00
```

### 2. Budget vs. Revenue

Calculates the Pearson correlation between budget and box office revenue and visualizes the relationship with a scatter plot.

```
Pearson correlation between budget and revenue: 0.75
```

![Budget vs Revenue](output/budget_revenue_scatter_plot.png)

### 3. Country Production Analysis

Ranks the top 5 countries by average revenue per film using `GROUP BY`, `AVG()`, and `JOIN` with the `movie_countries` junction table.

```
Top 5 Countries by Average Revenue:
     Country         Revenue
 New Zealand $757,910,728.75
         USA $378,280,444.02
   Australia $375,200,000.00
       Japan $260,800,000.00
South Africa $210,800,000.00
```

![Top 5 Countries](output/top_countries_avg_revenue_bar_plot.png)

### 4. Top 10 Films by Revenue

```
Top 10 Most Successful Movies by Revenue:
                 Movie Title           Revenue
                      Avatar $2,847,246,203.00
           Avengers: Endgame $2,798,000,000.00
    Avatar: The Way of Water $2,320,000,000.00
                     Titanic $2,194,439,542.00
Star Wars: The Force Awakens $2,068,000,000.00
      Avengers: Infinity War $2,048,000,000.00
     Spider-Man: No Way Home $1,910,000,000.00
              Jurassic World $1,671,000,000.00
               The Lion King $1,662,000,000.00
           Top Gun: Maverick $1,490,000,000.00
```

---

## 🧱 Architecture

| Layer      | File              | Responsibility                                              |
|------------|-------------------|-------------------------------------------------------------|
| Database   | `db/database.py`  | Schema creation, data loading, connection management        |
| Analysis   | `analysis.py`     | SQL queries, pandas aggregation, visualizations             |
| DDL ref    | `db/schema.sql`   | Portable schema reference (importable in any SQL client)    |

**Data flow:**

```
movies.csv → database.py → movies.db (SQLite) → analysis.py → terminal + output/*.png
```

---

## 🗄️ Database Schema

A normalized 9-table schema with junction tables for many-to-many relationships:

```
movie ──── movie_genres ──── genre
  │
  ├──────── movie_countries ── country
  │
  ├──────── movie_directors ── director
  │
  └──────── movie_languages ── language
```

---

## 🛡️ Error Handling

- Database connection errors are caught with `try/except` and the connection is always closed in a `finally` block
- Non-numeric `box_office` values (e.g. `'unknown'`) are excluded at the SQL level using `WHERE box_office != 'unknown'`
- `pd.to_numeric(..., errors='coerce')` is applied as an additional safeguard on the Python side

---

## 🛠️ Planned Improvements

- Add `pytest` unit tests for `database.py`
- Extend analysis with director and language breakdowns
- Add interactive visualizations with Plotly
- Connect to `movies-omdb-enrichment` pipeline as upstream data source

---

## 🧠 Technical Highlights

- **Normalized schema** — 9 tables with junction tables for M:N relationships (genre, country, director, language), ensuring 3NF compliance
- **Self-contained** — SQLite requires no server; the database is fully reproducible from `movies.csv`
- **Auto-initialization** — `setup_db()` checks for existing tables and initializes the database only if needed, making the project runnable with a single command
- **Data quality handling** — `'unknown'` values in `box_office` are filtered at the SQL level to avoid type errors and incorrect aggregations

---

## Changelog

### v1.0.0 — Initial Release

- Add normalized SQLite schema with 9 tables and junction tables
- Add `database.py` with connection management, schema creation, and data loading
- Add `setup_db()` for automatic database initialization on first run
- Add genre analysis — top 3 genres by total revenue
- Add budget-revenue analysis with Pearson correlation and scatter plot
- Add country production analysis — top 5 countries by average revenue with bar chart
- Add top 10 films by box office revenue

---

## Contributing

Contributions, suggestions, and feedback are welcome.

1. Fork the repository
2. Create a new branch:

```
git checkout -b feature/your-feature-name
```

3. Commit your changes:

```
git commit -m "feat: add your feature"
```

4. Push to your branch:

```
git push origin feature/your-feature-name
```

5. Open a Pull Request

If you spot a bug or have an idea, feel free to open an [issue](https://github.com/nicktm8/movies-sql-analytics/issues).