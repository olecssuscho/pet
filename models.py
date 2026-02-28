from pydantic import BaseModel

class TaskModels(BaseModel):
    id: int
    name: str
    description: str

