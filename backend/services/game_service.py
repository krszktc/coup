from random import choice, shuffle
import uuid

from models.constants import MAX_PLAYERS, GameType
from models.exceptions.exceptions import InfoException
from models.game_model import Game
from models.player_model import Player
from persistence import game_repo, user_repo, cards_repo


def create_game(user_id: str) -> Game:  
  cards = cards_repo.get_power_cards() \
      + cards_repo.get_power_cards() \
      + cards_repo.get_power_cards()
  shuffle(cards)
  player = Player(
    user_repo.find_by_id(user_id)
  )
  game = Game(
    id = str(uuid.uuid4()),
    cards = cards,
    players = [player],
    action_player = player,
  )
  return game_repo.save_game(game)


def add_player_to_game(game_id: str, user_id: str) -> Game:
  user = user_repo.find_by_id(user_id)
  game = game_repo.get_by_id(game_id)

  if len(game.players) >= MAX_PLAYERS :
    raise InfoException("Game already contain full set of users")
  elif game.state != GameType.INVITE:
    raise InfoException("Game no longer accept players to join")
  else:
    game.players.append(Player(user)) 

  return game


def start_game(game_id: str, user_id: str) -> Game:
  user = user_repo.find_by_id(user_id)
  game = game_repo.get_by_id(game_id)

  if game.state != GameType.INVITE:
    raise InfoException("Game already started")
  elif game.get_action_player_id() != user.id:
    raise InfoException("You can't change status for this game")
  else: 
    game.round_index = 1
    game.action_player = choice(game.players)
    for player in game.players:
      player.cards.append(game.cards.pop())
      player.cards.append(game.cards.pop())
      player.coins += 2
      game.coins -= 2

  return game


def get_game(game_id: str) -> Game:
  return game_repo.get_by_id(game_id)