from pydantic import BaseModel


class UserDao(BaseModel):
    id: str
    nick: str
    name: str

class UserDto(BaseModel):
    id: str
  