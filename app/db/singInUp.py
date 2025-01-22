import psycopg2
from fastapi import HTTPException

from app.db.conf import connector
from app.pwd_to_hash import check_password
from app.tokens import create_access_token


async def db_sing_in(email, password):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''
        SELECT id, email, password FROM users
        WHERE email = %s
        ''', (email, ))
        data = cur.fetchone()
        if data is None:
            return HTTPException(status_code=404, detail='No Such User')
        pwd = data[2]
        if not check_password(password, pwd):
            return HTTPException(status_code=401, detail='Incorrect password')
        return {'token': create_access_token({'id': data[0], 'email': data[1]})}
    except (Exception, psycopg2.DatabaseError) as e:
        return HTTPException(status_code=500, detail=f"DB error: {e}")
    finally:
        cur.close()
        conn.close()

async def db_sing_up(email, password):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''
            INSERT INTO users (email, password) VALUES (%s, %s)
            RETURNING id, email
        ''', (email, password))
        conn.commit()
        data = cur.fetchone()
        if data is None:
            raise HTTPException(status_code=500, detail='User creation failed')
        return {'token': create_access_token({'id': data[0], 'email': data[1]})}
    except psycopg2.IntegrityError as e:
        if 'unique constraint' in str(e).lower():
            raise HTTPException(status_code=400, detail="Email already exists")
        else:
            raise HTTPException(status_code=500, detail=f"DB error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {e}")
    finally:
        cur.close()
        conn.close()