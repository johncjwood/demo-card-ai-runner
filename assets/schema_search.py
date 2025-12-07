import sys
import psycopg2
import os

def search_schema(search_term):
    conn = psycopg2.connect(os.getenv('DATABASE_URL', 'postgresql://postgres:password1!@localhost:5432/cardapp'))
    cur = conn.cursor()
    
    cur.execute("""
        SELECT table_name, column_name 
        FROM information_schema.columns 
        WHERE table_schema = 'public' 
        AND (LOWER(table_name) LIKE LOWER(%s) OR LOWER(column_name) LIKE LOWER(%s))
        ORDER BY table_name, ordinal_position
    """, (f'%{search_term}%', f'%{search_term}%'))
    
    results = cur.fetchall()
    for table, column in results:
        print(f"{table}.{column}")
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python schema_search.py <search_term>")
        sys.exit(1)
    search_schema(sys.argv[1])
