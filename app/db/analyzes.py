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
        ORDER BY date DESC
        ''', (client_id,))
        response = [{
            "id": row[0],
            "date": row[1],
            "dep_total": row[2],
            "dep_stat": row[3].split('|'),
            "anx_total": row[4],
            "anx_stat": row[5].split('|')
            }
            for row in cur.fetchall()]
        return response
    except (Exception, psycopg2.DatabaseError) as e:
        return HTTPException(status_code=500, detail=f"DB error: {e}")
    finally:
        cur.close()
        conn.close()

async def db_add_analyse(
        date: str,
        client_id: int,
        dep_results: list,
        total_dep: int,
        anx_results: list,
        total_anx: int):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''
        INSERT INTO analyzes (client, date, depression_total, depression_stat, anxiety_total, anxiety_stat)
        VALUES (%s, %s, %s, %s, %s, %s)
        ''', (client_id, date, total_dep, '|'.join(map(str, dep_results)), total_anx, '|'.join(map(str, anx_results))))
        conn.commit()
        if cur.rowcount == 0:
            return HTTPException(status_code=400, detail=f"DB error: failed to add analyse")
        return HTTPException(status_code=200, detail=f"Analyse successfully added")
    except (Exception, psycopg2.DatabaseError) as e:
        return HTTPException(status_code=500, detail=f"DB error: {e}")
    finally:
        cur.close()
        conn.close()