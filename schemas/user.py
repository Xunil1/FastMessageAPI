from pydantic import BaseModel, Field



class UserCreate(BaseModel):
    username: str
    password: str = Field(..., min_length=4)