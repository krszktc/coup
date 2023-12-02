
from models.user import UserDao


USERS = [
  UserDao(id = '12345678-1111-1111-1111-123456123456', name = "First User", nick = "fUser"),
  UserDao(id = '12345678-2222-2222-2222-123456123456', name = "Second User", nick = "sUser"),
  UserDao(id = '12345678-3333-3333-3333-123456123456', name = "Third User", nick = "tUser"),
]

def find_by_id(uId: str) -> UserDao:
  return next([user for user in USERS if user.id == uId])