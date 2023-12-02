from models.card import Card
from persistence import cards_repo

def get_all() -> list[Card]:
  return cards_repo.get_all_cards()