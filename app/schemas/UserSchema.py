from pydantic import BaseModel

class UserSchema(BaseModel):
    name: str
    email: str
    password: str

class UserLoginSchema(BaseModel):
    email:str
    password:str