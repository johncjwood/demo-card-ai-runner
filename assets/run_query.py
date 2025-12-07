import sys
import psycopg2
import os

def run_query(query):
    conn = psycopg2.connect(os.getenv('DATABASE_URL', 'postgresql://postgres:password1!@localhost:5432/cardapp'))
    cur = conn.cursor()
    
    cur.execute(query)
    
    if cur.description:
        results = cur.fetchall()
        for row in results:
            print(row)
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python run_query.py '<query>'")
        sys.exit(1)
    run_query(sys.argv[1])
