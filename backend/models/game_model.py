from pydantic import BaseModel
from models.card import Card
from models.constants import MONEY_IN_BANK, ActionType, EffectType, GameType, DecisionType
from models.player_model import Player


class Game(BaseModel):
    id: str
    cards: list[Card]
    players: list[Player]
    coins: int = MONEY_IN_BANK

    action_player: Player
    target_player: Player | None = None
    contraction_player: Player | None = None
    power_loose_player: Player | None = None
    
    state: GameType = GameType.INVITE

    def get_active_card_action(this) -> ActionType:
        return this.action_player.claim.action
    
    def get_active_card_effect(this) -> EffectType:
        return this.action_player.claim.effect
    
    def get_player_by_id(this, id: str) -> Player:
        return next([player for player in this.players if player.user.id == id])
    
    def are_all_players_pass(this) -> bool:
        return len([player for player in this.players if player.decision != DecisionType.PASS]) > 0
    
    def clear_votes(this):
        for player in this.players:
            player.vote = None

    def is_over(this) -> bool:
        power_looser = [player for player in this.players if \
            player.cards[0].visible_for_others and player.cards[1].visible_for_others
        ]       
        return len(power_looser) > 0 


class GameDto(BaseModel):
    game_id: str
    player_id: str
    target_player_id: str | None = None
