from typing import Any
from data_model import PLAYER_NICKS, GAME_CARDS, GAME_ACTIONS, PromptResponse


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
  elif action == "chose" and value in GAME_CARDS:
    make_request("http://server_address/card", {"player": player, "card": value})
  elif action == "chose" and value in PLAYER_NICKS:
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
  elif action == "chose" and value in GAME_CARDS:
    make_request("http://server_address/card", {"player": player, "card": value})
  elif action == "chose" and value in PLAYER_NICKS:
    make_request("http://server_address/player", {"player": player, "target": value})
  else:
    print(f"I get following response: {response}")  


def parse_model(player_id: str, data: PromptResponse):
  if data.action == "N/A":
    make_request("http://server_address/pass", {"player": player_id, "target": data.target})
  elif data.action == "challenge":
    make_request("http://server_address/challenge", {"player": player_id, "target": data.target})
  elif data.action in GAME_ACTIONS:
    make_request(f"http://server_address/card/{data.action.lower()}", {"player": player_id, "target": data.target})
  else:
    print(f"I get following response: {data}")  


def make_request(*args):
  print(f"Make Request: {args}")