import http3

client = http3.AsyncClient()

def get_game(id: str):
  result = client.get(f'http://localhost:3000/game/status/{id}')
  return result.json


def get_cards():
  result = client.get(f'http://localhost:3000/cards')
  return result


def raise_card(card_code: str):
  result = client.post(f'http://localhost:3000/player/{card_code}')
  return result


def raise_pass():
  result = client.post(f'http://localhost:3000/player/pass')
  return result


def raise_challenge():
  result = client.post(f'http://localhost:3000/player/challenge')
  return result


