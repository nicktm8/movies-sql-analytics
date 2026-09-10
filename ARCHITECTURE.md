# Architecture – movies-sql-analytics

## Overview

A self-contained analytics project built on a normalized SQLite database.
Raw CSV data is loaded into a relational schema via `database.py`, then queried
through `analysis.py` using SQL and Python (pandas, Matplotlib, Seaborn)
to produce financial and production insights.

---

## Project Structure

```
movies-sql-analytics/
│
├── assets/
│   ├── budget_revenue_scatter_plot.png
│   └── top_countries_avg_revenue_bar_plot.png
|
├── data/
│   └── movies.csv              # Source dataset (raw movie data)
│
├── db/
│   ├── database.py             # get_connection(), create_tables(), insert_data(), setup_db()
│   └── schema.sql              # DDL reference (CREATE TABLE statements)
│
├── output/
│   ├── scatter_plot.png        # Budget vs. revenue scatter plot (generated)
│   └── bar_plot.png            # Top 5 countries bar chart (generated)
│
├── analysis.py                 # SQL queries + pandas analysis + visualizations
├── requirements.txt
├── .gitignore                  # Excludes movies.db and output/
└── README.md
```

> `movies.db` is excluded from version control — it is generated locally
> by running `python analysis.py` (which calls `setup_db()` automatically)
> or directly via `python db/database.py`. See [Getting Started](README.md#getting-started) in README.

---

## Data Flow

```
movies.csv
    |
    | pandas read_csv
    v
db/database.py ──── CREATE TABLE / INSERT ────> movies.db (SQLite)
                                                      |
                                                      | pd.read_sql_query
                                                      v
                                                analysis.py
                                                      |
                                   +------------------+------------------+
                                   |                                     |
                             pandas aggregation               Matplotlib / Seaborn
                                   |                                     |
                             Terminal output                       output/*.png
```

> `setup_db()` in `database.py` acts as a guard — it verifies that the
> database exists and contains data before `analysis.py` runs any queries.

---

## Database Schema

The database follows a normalized relational model with junction tables
to handle many-to-many relationships between movies and their attributes.

```
movie ──────────────── movie_genres ─────── genre
  │
  ├─────────────────── movie_countries ───── country
  │
  ├─────────────────── movie_directors ───── director
  │
  └─────────────────── movie_languages ───── language
```

| Table              | Description                              | Key columns                                  |
|--------------------|------------------------------------------|----------------------------------------------|
| `movie`            | Core film data                           | `movie_id`, `title`, `budget`, `box_office`  |
| `genre`            | Genre lookup                             | `genre_id`, `name`                           |
| `country`          | Country lookup                           | `country_id`, `name`                         |
| `director`         | Director lookup                          | `director_id`, `name`                        |
| `language`         | Language lookup                          | `language_id`, `name`                        |
| `movie_genres`     | Movie ↔ Genre (M:N)                      | `movie_id`, `genre_id`                       |
| `movie_countries`  | Movie ↔ Country (M:N)                    | `movie_id`, `country_id`                     |
| `movie_directors`  | Movie ↔ Director (M:N)                   | `movie_id`, `director_id`                    |
| `movie_languages`  | Movie ↔ Language (M:N)                   | `movie_id`, `language_id`                    |

---

## Module Descriptions

### `db/database.py`

Single entry point for all database operations — connection, schema creation,
data loading, and initialization guard.

| Function              | Description                                                                     |
|-----------------------|---------------------------------------------------------------------------------|
| `get_connection()`    | Returns a `sqlite3.Connection` to `movies.db`                                   |
| `create_tables(conn)` | Executes DDL — creates all 9 tables if they do not exist                        |
| `insert_data(conn)`   | Reads CSV via pandas, populates all tables                                      |
| `setup_db()`          | Verifies database exists and contains data; initializes it if not; prints stats |

### `analysis.py`

Executes four analytical queries and produces visualizations.
Calls `setup_db()` at startup to ensure the database is ready before any queries run.

| Section                        | SQL features used              | Python output                  |
|--------------------------------|--------------------------------|--------------------------------|
| Genre analysis (top 3)         | JOIN, GROUP BY, SUM, ORDER BY  | Table (terminal)               |
| Budget vs. revenue             | SELECT, AVG                    | Scatter plot, Pearson r        |
| Country analysis (top 5)       | JOIN, GROUP BY, AVG, ORDER BY  | Bar chart                      |
| Top 10 films by revenue        | ORDER BY, LIMIT                | Table (terminal)               |

---

## Technology Stack

| Layer         | Technology                          |
|---------------|-------------------------------------|
| Database      | SQLite 3 (via `sqlite3` stdlib)     |
| Data loading  | pandas `read_csv`, `read_sql_query` |
| Visualization | Matplotlib, Seaborn                 |
| Language      | Python 3.x                          |

---

## Design Decisions

**SQLite over MySQL** — No server required. The database is fully
reproducible from `movies.csv` by running `analysis.py`, making the
project portable and easy to run locally without any configuration.

**Junction tables** — Many-to-many relationships (e.g. a film can belong
to multiple genres) are resolved through explicit junction tables rather
than storing comma-separated values, ensuring the schema is in 3NF.

**Single database module** — All database logic is consolidated in
`db/database.py` (`get_connection`, `create_tables`, `insert_data`,
`setup_db`). An earlier iteration had a separate `setup_db.py` module,
but this caused import path conflicts between the `db/` package and
the `db.py` module name. Consolidating into one module simplified imports
and removed the naming ambiguity.

**Separation of concerns** — Database logic (`database.py`) is isolated
from analysis logic (`analysis.py`), following the same modular pattern
used in the `movies-omdb-enrichment` pipeline.
