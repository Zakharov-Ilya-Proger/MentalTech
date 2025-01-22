from http.client import responses
from typing import Annotated
from fastapi import APIRouter, Header, HTTPException

from app.db.clients import db_get_all, db_add_client
from app.models import AddUser
from app.tokens import decode_token

clients = APIRouter()


@clients.get("/get")
async def get_clients(Authorization: Annotated[str | None, Header()] = None):
    token = decode_token(Authorization)
    response = await db_get_all(token['id'])
    if isinstance(response, HTTPException):
        raise response
    return response

@clients.post("/add")
async def add_clients(user: AddUser, Authorization: Annotated[str | None, Header()] = None):
    token = decode_token(Authorization)
    response = await db_add_client(user.username, token['id'])
    raise response
