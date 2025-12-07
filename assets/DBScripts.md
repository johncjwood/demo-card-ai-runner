# Database Scripts

## schema_search.py
Searches for tables and columns in the database schema using case-insensitive matching.

**Usage:**
```bash
python schema_search.py <search_term>
```

**Example:**
```bash
python schema_search.py user
```

## run_query.py
Executes a SQL query on the database and displays results.

**Usage:**
```bash
python run_query.py '<query>'
```

**Example:**
```bash
python run_query.py 'SELECT * FROM users LIMIT 5'
```

**Important:** This script should be used for read-only queries only. Any persistent database changes should be made in `./db/99 Additional.sql`.
