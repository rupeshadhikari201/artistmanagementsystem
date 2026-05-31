import psycopg2 
import psycopg2.extras
from decouple import config 


def get_connection():
    
    connection = psycopg2.connect(config('DATABASE_URL'))
    return connection

def execute(sql, params=(), fetch=None):
    
    with get_connection() as connection:
        with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(sql,params)
            connection.commit()
            
            if fetch == 'one':
                row = cursor.fetchone()
                return dict(row) if row else None
            
            if fetch == 'all':
                rows = cursor.fetchall()
                return [dict[r] for r in rows]
            
            return cursor.rowcount