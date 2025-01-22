import psycopg2
from fastapi import HTTPException

from app.db.conf import connector


async def db_get_analyzes(client_id):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''
        SELECT id, date, depression_total, depression_stat, anxiety_total, anxiety_stat 
        FROM analyzes
        WHERE client = %s
        ORDER BY date
        ''', (client_id,))
        response = [{
            "id": row[0],
            "date": row[1],
            "dep_total": row[2],
            "dep_stat": row[3],
            "anx_total": row[4],
            "anx_stat": row[5]
            }
            for row in cur.fetchall()]
        return response
    except (Exception, psycopg2.DatabaseError) as e:
        return HTTPException(status_code=500, detail=f"DB error: {e}")
    finally:
        cur.close()
        conn.close()