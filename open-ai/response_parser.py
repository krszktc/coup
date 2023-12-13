from typing import Any

# Take from db after init request for AI to play in the game
cards = ["Duke", "Assassin", "Ambassador", "Captain", "Contessa"]
players = ["PlayerA", "PlayerB", "PlayerC"]


def parse_string(response: str):
  data = response.split(" ")
  player = data[0]
  action = data[1]
  value = data[2] if len(data) == 3 else None

  if action == "pass":
    make_request("http://server_address/pass", {"player": player})
  elif action == "challenge":
    make_request("http://server_address/challenge", {"player": player})
  elif action == "claim":
    make_request("http://server_address/claim", {"player": player})
  elif action == "chose" and value in cards:
    make_request("http://server_address/card", {"player": player, "card": value})
  elif action == "chose" and value in player:
    make_request("http://server_address/player", {"player": player, "target": value})
  else:
    print(f"I get following response: {response}")
  

def parse_json(response: Any):
  player = response["player"]
  action = response["action"]
  value = response["value"]

  if action == "pass":
    make_request("http://server_address/pass", {"player": player})
  elif action == "challenge":
    make_request("http://server_address/challenge", {"player": player})
  elif action == "claim":
    make_request("http://server_address/claim", {"player": player})
  elif action == "chose" and value in cards:
    make_request("http://server_address/card", {"player": player, "card": value})
  elif action == "chose" and value in player:
    make_request("http://server_address/player", {"player": player, "target": value})
  else:
    print(f"I get following response: {response}")  


def make_request(*args):
  print(f"Make Request: {args}")