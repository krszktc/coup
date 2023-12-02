from models.constants import GameType, DecisionType
from models.exceptions.info_exception import InfoException
from models.game_model import GameDto
from persistence import game_repo, cards_repo
from services import effect_service


def raise_card(card_code: str, dto: GameDto):
  (game, player) = __get_game_player_tuple(dto)
  card = cards_repo.get_by_code(card_code)
  target_player = game.get_player_by_id(dto.target_player_id)

  def set_power_loose():
    effect_service.loose_power(player, card)
    if game.is_over():
      game.state = GameType.END
      return f"Player: {player.user.nick} loosed" 

  if game.action_player == player and game.state == GameType.ACTION:
    if not card.can_be_blocked:
      effect_service.apply(game)
      effect_service.next_round(game)
    else:
      player.claim = card
      game.target_player = target_player
      game.state = GameType.ACTION_CHECK

  elif game.state == GameType.CONTRACTION:
    if game.get_active_card_action() == card.contraction:
      player.claim = card
      game.contraction_player = player
      game.state = GameType.CONTRACTION_CHECK
    else:
      raise InfoException("You can't contraction raising this card. Check games status.")  

  elif game.power_loose_player == player and game.state == GameType.ACTION_POWER_LOSE:
    set_power_loose()
    if game.action_player == player:
      effect_service.next_round(game)
    else:
      game.state = GameType.CONTRACTION

  elif game.power_loose_player == player and game.state == GameType.CONTRACTION_POWER_LOSE:
    set_power_loose()
    effect_service.apply(game)
    effect_service.next_round(game)

  elif game.target_player == player and game.state == GameType.EFFECT_POWER_LOSE:
    set_power_loose()
    effect_service.next_round(game)

  else:  
    raise InfoException("You can't raise the card now. Check games status.")  
  return f"Player: {player.user.nick} raised card {card.code}"  


def decision_pass(dto: GameDto):
  (game, player) = __get_game_player_tuple(dto)

  if game.state == GameType.ACTION_CHECK:
    player.decision = DecisionType.PASS
    if game.are_all_players_pass():
      game.clear_votes()
      game.state = GameType.CONTRACTION

  elif game.state == GameType.CONTRACTION:
    player.decision = DecisionType.PASS
    if game.are_all_players_pass():
      effect_service.apply(game)
      effect_service.next_round(game)  

  elif game.state == GameType.CONTRACTION_CHECK:
    player.decision = DecisionType.PASS
    if game.are_all_players_pass():
      effect_service.pay_for_blocked_action(game)
      effect_service.next_round(game)  
  
  else:  
    raise InfoException("You can't pass now. Check games status.")  
  return f"Player: {player.user.nick} passed"


def challenge(dto: GameDto):
  (game, player) = __get_game_player_tuple(dto)

  if game.state == GameType.ACTION_CHECK:
    game.state = GameType.ACTION_POWER_LOSE
    if game.action_player.has_claimed():
      game.power_loose_player = player
    else:
      game.power_loose_player = game.active_player

  elif game.state == GameType.CONTRACTION_CHECK:
    game.state = GameType.CONTRACTION_POWER_LOSE
    if game.contraction_player.has_claimed():
      game.power_loose_player = player
    else:
      game.power_loose_player = game.contraction_player  

  else:  
    raise InfoException("You can't challenge now. Check games status.")
  return f"Player: {player.user.nick} post challenge"


def __get_game_player_tuple(game_dto: GameDto):
  game = game_repo.get_by_id(game_dto.game_id)
  player = game.get_player_by_id(game_dto.player_id)
  return (game, player)
