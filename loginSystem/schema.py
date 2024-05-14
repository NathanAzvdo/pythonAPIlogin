from pydantic import BaseModel

class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    Eadmin: int = 0