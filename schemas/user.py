from pydantic import BaseModel, Field

class User(BaseModel):
    username: str
    password: str = Field(..., min_length=4)

class UserCreate(User):
    pass