
from models.game_model import Game


GAMES: list[Game] = []


def save_game(game: Game) -> Game:
  GAMES.append(game)
  return game


def get_by_id(gId: str) -> Game:
  return next([game for game in GAMES if game.id == gId])