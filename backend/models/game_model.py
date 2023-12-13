from pydantic import BaseModel
from models.card import Card
from models.constants import MONEY_IN_BANK, ActionType, EffectType, GameStatus, DecisionType
from models.player_model import Player


class Game(BaseModel):
    id: str
    cards: list[Card]
    players: list[Player]
    coins: int = MONEY_IN_BANK

    action_player: Player
    contraction_player: Player | None = None
    power_loose_player: Player | None = None
    
    round_steps = [
        GameStatus.INVITE,
        GameStatus.ACTION,
        GameStatus.CHALLENGE,
        GameStatus.CONTRACTION,
        GameStatus.CHALLENGE,
        GameStatus.END,
    ]

    round_index = 0


    @property
    def status(this) -> GameStatus:
        this.round_steps[this.round_index]


    def get_player(this, id: str) -> Player:
        return next([player for player in this.players if player.user.id == id])


    def get_challenged_player(this) -> Player:
        if this.round_steps[this.round_index -1] == GameStatus.ACTION:
            return this.action_player
        return this.contraction_player
    

    def get_active_card_action(this) -> ActionType:
        return this.action_player.claim.action
    

    def are_all_players_pass(this) -> bool:
        return len([player for player in this.players if player.decision != DecisionType.PASS]) == 0


    def next_step(this):
        this.power_loose_player = None
        this.__clear_votes()
        if this.round_steps[this.round_index +1] == GameStatus.END:
            this.execute_action()
            this.round_index = 1
        else:
            this.round_index += 1     


    def player_out(this):    
        losers = [player for player in this.players if player.is_looser]
        if len(losers) == len(this.players) -1:
            this.round_index = len(this.round_steps) -1 
        elif this.action_player in losers or this.game.contraction_player in losers:
            this.__next_round()
        else:
            this.next_step()


    def execute_action(this):
        # effect_service.something()
        this.__next_round()


    def power_loosed(this):
        pass    
                

    def exchange_card(this, player: Player, card: Card):
        this.cards.insert(0, card)
        player.cards.append(this.cards.pop())


    def __next_round(this):
        this.action_player = [player for player in this.players if not player.is_looser][0]
        this.contraction_player = None
        this.power_loose_player = None
        this.__clear_votes(True)


    def __clear_votes(this, include_claim = False):
        for player in this.players:
            if include_claim:
                player.claim = None
            if player == this.action_player:
                player.decision = DecisionType.PASS
            else:
                player.decision = None
        





    def get_active_card_effect(this) -> EffectType:
        return this.action_player.claim.effect
    

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


class ActionDto(GameDto):
    contraction_player_id: str | None

