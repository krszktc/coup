
from random import shuffle
from models.card import Card
from models.constants import EffectType, GameType
from models.exceptions.info_exception import InfoException
from models.game_model import Game
from models.player_model import Player


def apply(game: Game):
  effect = game.get_active_card_effect()
  if effect == None:
     raise InfoException("Oppps! Looks like you raised no-effect card") 
  elif effect == EffectType.TAKE1: __take_1_coin(game)
  elif effect == EffectType.TAKE2: __take_2_Coins(game)
  elif effect == EffectType.PAY7: __pay_7_coins(game)
  elif effect == EffectType.TAKE3: __take_3_coins(game)
  elif effect == EffectType.PAY3: __pay_3_coins(game)
  elif effect == EffectType.EXCHANGE:__exchange_ards(game)
  elif effect == EffectType.STEAL2: __steal_2_coins(game)


def next_round(game: Game):
  if game.is_over():
    raise InfoException("Game is over") 
  game.clear_votes()
  game.target_player = None
  game.contraction_player = None
  game.power_loose_player = None
  active_player_index = game.players.index(game.action_player)
  if active_player_index == len(game.players -1):
    game.action_player = game.players[0]
  else:
    game.action_player = game.players[active_player_index + 1]


def loose_power(player: Player, card: Card):
  loose_cards = [pCard for pCard in player.cards if pCard.code == card.code]
  if len(loose_cards) > 0:
    loose_cards[0].visible_for_others = True
  else:
    raise InfoException("You don't have requested card.") 
  

def pay_for_blocked_action(game: Game):
  effect = game.get_active_card_effect()
  if effect != EffectType.PAY3:
     raise InfoException("You don't need to pay for this action") 
  __pay_3_coins(game, False)


def __take_1_coin(game: Game):
  game.action_player.coins += 1
  game.coins -= 1


def __take_2_Coins(game: Game):
  game.action_player.coins += 2
  game.coins -= 2


def __pay_7_coins(game: Game):
  if game.target_player == None:
    raise InfoException("COUP require target player to be defined") 
  game.coins += 7
  game.action_player.coins -= 7
  game.state = GameType.EFFECT_POWER_LOSE


def __take_3_coins(game: Game):
  game.action_player.coins += 3
  game.coins -= 3


def __pay_3_coins(game: Game, change_state = True):
  if game.target_player == None:
    raise InfoException("Assassinate require target player to be defined") 
  if change_state:
    game.state = GameType.EFFECT_POWER_LOSE
  game.coins += 3
  game.action_player.coins -= 3
  

def __exchange_ards(game: Game):
  stock = game.cards + game.action_player.cards
  shuffle(stock)
  game.action_player.cards = []
  game.action_player.cards.append(game.cards.pop())
  game.action_player.cards.append(game.cards.pop())


def __steal_2_coins(game: Game):
  if game.target_player == None:
    raise InfoException("Steal require target player to be defined") 
  elif game.target_player.coins < 2:
    raise InfoException("Target player has less than 2 coins to steal") 
  game.target_player.coins -= 2
  game.action_player.coins += 2