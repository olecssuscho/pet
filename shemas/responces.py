from pydantic import ConfigDict,BaseModel

class TaskResponse(BaseModel):
   model_config = ConfigDict(from_attributes=True)
   
   id: int
   name: str
   description: str
   status: str  


class UserResponse(BaseModel):
   model_config = ConfigDict(from_attributes=True)
   
   login: str   