from models.constants import ActionType, EffectType
from pydantic import BaseModel


class Card(BaseModel):
    code: str
    visible_for_others: bool = False
    default_color: str | None = None
    character_name: str | None = None
    action: ActionType | None = None
    effect: EffectType | None = None
    contraction: ActionType | None = None
    