from random import choice
from storage import app_storage
import request_service

def get_games():
  return app_storage.get_games()


def save_game(game_id: str, user_id: str):
  users = app_storage.get_game_by_id(game_id)
  if users:
    users.append(user_id)
  else:
    app_storage.save_game({game_id: [user_id]})


def save_cards(cards):
  app_storage.save_cards(cards)


def get_cards():
  return app_storage.get_cards()


def supervise():
  for game_id, game_users in get_games():
    game = request_service.get_game(game_id)
    if game.state == 'ACTION' and game.action_player in game_users:
      __decide_action()
    elif game.state == 'ACTION_CHECK' or game.state == 'CONTRACTION_CHECK':
      __decide_challenge_or_pass()
    elif (game.state == 'ACTION_POWER_LOSE' or 
        game.state == 'CONTRACTION_POWER_LOSE' or 
        game.state == 'EFFECT_POWER_LOSE') and game.power_loose_player in game_users:
      __decide_power_loose(game.power_loose_player)
    elif game.state == 'CONTRACTION' and game.contraction_player in game_users:
      __decide_contraction(game)


def __decide_action():
  playable_cards = [card for card in get_cards() if card.code != "cn"]
  request_service.raise_card(choice(playable_cards))


def __decide_challenge_or_pass():
  if choice([0,1]) == 0:
    request_service.raise_pass()
  else:
    request_service.raise_challenge()


def __decide_power_loose(player):
  request_service.raise_card(choice(player.cards))


def __decide_contraction(game):
  active_card = game.action_player.claim
  block_cards = [card for card in get_cards() if card.contraction == active_card.action]
  my_cards = game.contraction_player.cards
  my_block_cards = [card for card in my_cards if card in block_cards]

  should_lie = choice([0,1]) == 0

  if len(my_cards) > 0:
    request_service.raise_card(choice(my_block_cards))
  elif len(block_cards) > 0 and should_lie:
    request_service.raise_card(choice(block_cards))
  else:
    request_service.raise_pass()  