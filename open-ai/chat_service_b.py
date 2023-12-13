import json
from openai import OpenAI
import response_parser

client = OpenAI()

# Statefull service AntiPattern, don't do this on prod!!!
# Thread represent Game
game_progress: list[str] = []
player_b_cards = ["Duke", "Assassin"]
player_c_cards = ["Duke", "Ambassador"]


def mock_string_progress(mock_messages: list[str]):
	# any logic here to emulate GameServer state
	game_progress.extend(mock_messages)
	request_messages = [
		{
			"role": "system", 
			"content": f"""We play COUP card game. You play as PlayerB and PlayerC. 
										PlayerA has {player_b_cards[0]} card and {player_b_cards[1]} card
										PlayerB has {player_c_cards[0]} card and {player_c_cards[1]} card"""
		}
	] + [
		{"role": "user", "content": message} for message in game_progress
	]
	completion = client.chat.completions.create(
		model="ft:gpt-3.5-turbo-1106:hops::8UyaBRkC",
		messages=request_messages
	)
	response_message = completion.choices[0].message.content
	response_parser.parse_string(response_message)
	game_progress.append(response_message)

	print(f"Game progress: {game_progress}")
	print("----------------------------")


def mock_json_process(mock_messages: list[str]):
	# any logic here to emulate GameServer state
	game_progress.extend(mock_messages)
	triple_response = '{"player": "PlayerB", "action": "chose", "value": "UserA"}'
	double_response = '{"player": "PlayerB", "action": "pass", "value": ""}'
	request_messages = [
		{
			"role": "system", 
			"content": f"""We play COUP card game. You play as PlayerB and PlayerC. 
										PlayerA has {player_b_cards[0]} card and {player_b_cards[1]} card.
										PlayerB has {player_c_cards[0]} card and {player_c_cards[1]} card. 
										Give response in JSON format like {triple_response} fro three worlds response
										or like {double_response} for two worlds response"""
		}
	] + [
		{"role": "user", "content": message} for message in game_progress
	]
	completion = client.chat.completions.create(
		model="ft:gpt-3.5-turbo-1106:hops::8UyaBRkC",
		response_format={ "type": "json_object" },
		messages=request_messages
	)
	response_message = json.loads(completion.choices[0].message.content)
	response_parser.parse_json(response_message)
	game_progress.append(f"{response_message["player"]} {response_message["action"]} {response_message["value"]}")

	print(f"Game progress: {game_progress}")
	print("----------------------------")
