from pydantic import BaseModel
from models.exceptions.exceptions import DataModelException
from models.card import Card
from models.constants import DecisionType
from .user import UserDao


class Player(BaseModel):
    user: UserDao
    coins: int = 0
    cards: list[Card] = []
    claim: Card | None = None
    decision: DecisionType | None = None

   
    @property
    def is_looser(this) -> bool:
        return len(this.get_playable_cards()) == 0
    

    @property
    def can_be_challenged(this) -> bool:
        return this.claim and this.claim.character_name
    

    def get_claimed(this) -> Card | None:
        claimed_cards = this.__get_card(this.claim)
        if len(claimed_cards) > 0:
            first_claimed = claimed_cards[0]
            this.cards.remove(first_claimed)
            return first_claimed
    

    def loose_power(this, power_card: Card):
        power_loose_card = this.__get_card(power_card)
        if len(power_loose_card) > 0:
            power_loose_card[0].visible_for_others = True
            this.claim = None
        else:
            raise DataModelException("Requested card can't be loosed cards")      


    def get_playable_cards(this) -> list[Card]:
        return [card for card in this.cards if not card.visible_for_others]


    def __get_card(this, card_to_check: Card) -> list[Card]:
       return [card for card in this.cards if card.code == card_to_check.code]
    

   


class PlayerActionDto(BaseModel):
    operation: str    
    status: str = "complete"
    