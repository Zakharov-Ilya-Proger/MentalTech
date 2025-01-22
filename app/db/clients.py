import psycopg2
from fastapi import HTTPException

from app.db.conf import connector


async def db_get_all(doctor_id):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''
        SELECT id, name
        FROM clients
        WHERE doctor = %s
        ORDER BY name
        ''', (doctor_id,))
        data = [{'id': row[0], "name": row[1]} for row in cur.fetchall()]
        return data
    except (Exception, psycopg2.DatabaseError) as e:
        raise HTTPException(status_code=500, detail=str(f"DB error: {e}"))
    finally:
        cur.close()
        conn.close()

async def db_add_client(client_name, doctor_id):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''
        INSERT INTO clients (name, doctor) VALUES (%s, %s)
        ''', (client_name, doctor_id))
        conn.commit()
        if cur.rowcount == 0:
            return HTTPException(status_code=404, detail="Client not found")
        return HTTPException(status_code=200, detail=f"Client {client_name} added")
    except (Exception, psycopg2.DatabaseError) as e:
        return HTTPException(status_code=500, detail=str(f"DB error: {e}"))
    finally:
        conn.close()
        cur.close()