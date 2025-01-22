from fastapi import APIRouter, HTTPException
from app.db.singInUp import db_sing_in, db_sing_up
from app.models import SingIn
from app.pwd_to_hash import hash_password

sing = APIRouter()

@sing.post("/in")
async def sing_in(user: SingIn):
    response = await db_sing_in(user.email, user.password)
    if isinstance(response, HTTPException):
        raise response
    return response


@sing.post("/up")
async def sing_up(user: SingIn):
    response = await db_sing_up(user.email, hash_password(user.password))
    if isinstance(response, HTTPException):
        raise response
    return response