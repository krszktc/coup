from models.card import Card
from models.constants import ActionType, EffectType

# cached
def get_power_cards() -> list[Card]: 
  return [
    Card(code = "du", character_name = 'Duke', default_color = "red",
      action = ActionType.TAX, effect = EffectType.TAKE3, contraction = ActionType.FOREIGN_AID, can_be_blocked = False
    ),
    Card(code = "as", character_name = 'Assassin', default_color = "brown",
      action = ActionType.ASSASSINATE, effect = EffectType.PAY3, can_be_blocked = True
    ),
    Card(code = "am", character_name = 'Ambassador', default_color = "yellow",
      action = ActionType.EXCHANGE, effect = EffectType.EXCHANGE, contraction = ActionType.STEAL, can_be_blocked = False
    ),
    Card(code = "cp", character_name = 'Captain', default_color = "blue",
      action = ActionType.STEAL, effect = EffectType.TAKE2, contraction = ActionType.STEAL, can_be_blocked = True
    ),
    Card(code = "cn", character_name = 'Contessa', default_color = "orange",
      contraction = ActionType.ASSASSINATE, can_be_blocked = False
    ),
  ]

# cached
def get_basic_cards() -> list[Card]:
  return [
    Card(code = "e1", action = ActionType.INCOME, effect = EffectType.TAKE1, can_be_blocked = False),
    Card(code = "e2", action = ActionType.FOREIGN_AID, effect = EffectType.TAKE2, can_be_blocked = True),
    Card(code = "e3", action = ActionType.COUP, effect = EffectType.PAY7, can_be_blocked = False),
  ]

# cached
def get_all_cards() -> list[Card]:
  return get_power_cards() + get_basic_cards()

# cached
def get_by_code(code: str) -> Card:
  return next([card for card in get_all_cards() if card.code == code])
