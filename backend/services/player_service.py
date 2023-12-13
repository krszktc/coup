from models.constants import COINS_TO_CALL_COUP, COUP_CARD_CODE, ONE_INCOME_CARD_CODE, GameStatus, DecisionType
from models.exceptions.exceptions import InfoException
from models.game_model import Game, GameDto, ActionDto, Player
from persistence import game_repo, cards_repo


def action(card_code: str, dto: ActionDto):
  (game, player) = __get_game_and_player_tuple(dto)
  
  if player == game.action_player and game.status == GameStatus.ACTION:
    code = COUP_CARD_CODE if len(player.coins) >= COINS_TO_CALL_COUP else card_code
    player.claim = cards_repo.get_by_code(code)

    if player.claim == COUP_CARD_CODE or player.claim == ONE_INCOME_CARD_CODE:
      game.execute_action()
    else:
      game.contraction_player = __get_game_player(game, dto.contraction_player_id)
      game.next_step()

  else:
    raise InfoException("You can't raise the card now. Check games status.")  


def card(card_code: str, dto: GameDto):
  (game, player) = __get_game_and_player_tuple(dto)
  card = cards_repo.get_by_code(card_code)

  if player == game.power_loose_player:
    player.loose_power(card)
    game.power_loosed() # ???
  
  elif game.status == GameStatus.CONTRACTION:
    if game.contraction_player == None:
      game.contraction_player = player
    elif game.contraction_player != player:
      raise InfoException("Contraction player already set. Check games status.") 
    
    if game.contraction_player.claim != None:
      raise InfoException("Contraction already set. Check games status.") 
    if card.contraction != game.get_active_card_action():
      raise InfoException("You can't use this card for Contraction. Check games status.")
    
    player.claim = card
    game.next_step()

  else:
    raise InfoException("You can't set contraction now. Check games status.")    


def decision_pass(dto: GameDto):
  (game, player) = __get_game_and_player_tuple(dto)

  if game.status == GameStatus.CHALLENGE:
    player.decision = DecisionType.PASS
    if game.are_all_players_pass():
      game.next_step()

  if game.status == GameStatus.CONTRACTION:
    game.execute_action()

  else:
    raise InfoException("You can't pass. Check games status.")  


def decision_challenge(dto: GameDto):
  (game, player) = __get_game_and_player_tuple(dto)
  power_loose_player = game.power_loose_player
  
  if power_loose_player == None and game.status == GameStatus.CHALLENGE:
    challenged_player = game.get_challenged_player()
    if not challenged_player.can_be_challenged:
      raise InfoException("You can challenge now. Check games status.") 

    challenged_card = challenged_player.get_claimed()
    if challenged_card:
      game.exchange_card(challenged_player, challenged_card)
      power_loose_player = player
    else:
      power_loose_player = challenged_player  

    looser_playable_cards = power_loose_player.get_playable_cards()
    if len(looser_playable_cards) == 1:
      power_loose_player.loose_power(looser_playable_cards[0])
      game.player_out()
    else:  
      game.power_loose_player = power_loose_player

  else:
    raise InfoException("You can't challenge. Check games status.")
  
    
def __get_game_and_player_tuple(dto: GameDto) -> tuple[Game, Player]:
  game = game_repo.get_by_id(dto.game_id)
  if game == None:
    raise InfoException(f"Game {dto.game_id} doesn't exist.")  
  player = __get_game_player(game, dto.player_id)

  return (game, player)


def __get_game_player(game: Game, player_id: str | None) -> Player | None:
  if player_id == None:
    return None 

  player = game.get_player(player_id)
  if player == None:
    raise InfoException(f"Player {player_id} does't play game {game.id}")    
  if player.is_looser:
    raise InfoException(f"Player {player_id} already lost all influences")    

  return player