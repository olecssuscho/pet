from pydantic import BaseModel
from typing import Literal

class TaskModels(BaseModel):

    name: str
    description: str
    status:Literal["new", "in_progress", "done"] = "new"

class UserModels(BaseModel):
   
    login: str
    password: str

