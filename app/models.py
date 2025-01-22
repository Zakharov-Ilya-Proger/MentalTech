from pydantic import BaseModel


class SingIn(BaseModel):
    password: str
    email: str

class AddUser(BaseModel):
    username: str