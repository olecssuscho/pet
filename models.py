from pydantic import BaseModel

class TaskModels(BaseModel):

    name: str
    description: str

class UserModels(BaseModel):
   
    login: str
    password: str
