from models.card import Card
from models.constants import ActionType, EffectType


def get_power_cards() -> list[Card]: 
  return [
    Card(code = "du", character_name = 'Duke', default_color = "red",
      action = ActionType.TAX, effect = EffectType.TAKE3, contraction = ActionType.FOREIGN_AID,
    ),
    Card(code = "as", character_name = 'Assassin', default_color = "brown",
      action = ActionType.ASSASSINATE, effect = EffectType.PAY3,
    ),
    Card(code = "am", character_name = 'Ambassador', default_color = "yellow",
      action = ActionType.EXCHANGE, effect = EffectType.EXCHANGE, contraction = ActionType.STEAL,
    ),
    Card(code = "cp", character_name = 'Captain', default_color = "blue",
      action = ActionType.STEAL, effect = EffectType.TAKE2, contraction = ActionType.STEAL,
    ),
    Card(code = "cn", character_name = 'Contessa', default_color = "orange",
      contraction = ActionType.ASSASSINATE,
    ),
  ]


def get_basic_cards() -> list[Card]:
  return [
    Card(code = "e1", action = ActionType.INCOME, effect = EffectType.TAKE1),
    Card(code = "e2", action = ActionType.FOREIGN_AID, effect = EffectType.TAKE2),
    Card(code = "e3", action = ActionType.COUP, effect = EffectType.PAY7),
  ]


def get_all_cards() -> list[Card]:
  return get_power_cards() + get_basic_cards()


def get_by_code(code: str) -> Card:
  return next([card for card in get_all_cards() if card.code == code])


def get_blocking(card: Card) -> list[Card]:
  return [db_card for db_card in get_all_cards() if db_card.contraction == card.action]