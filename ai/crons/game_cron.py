from fastapi_utils.tasks import repeat_every
from services import game_service


@repeat_every(seconds=10)
def check_games():
  game_service.supervise()