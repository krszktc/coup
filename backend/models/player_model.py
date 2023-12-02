from pydantic import BaseModel
from models.card import Card
from models.constants import DecisionType
from .user import UserDao


class Player(BaseModel):
    user: UserDao
    coins: int = 0
    cards: list[Card] = []
    claim: Card | None = None
    decision: DecisionType = DecisionType.PASS

    def has_claimed(this) -> bool:
        return len([card for card in this.cards if card.code == this.claim.code]) > 0
    

class PlayerActionDto(BaseModel):
    operation: str    
    status: str = "complete"
    