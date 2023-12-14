import json
import response_parser
from openai import OpenAI
from data_model import GAME_LOGS, PLAYERS, GameLog, Player, PromptResponse

client = OpenAI()


def mock_progress():
	players_info = ". ".join([__get_player_info(player) for player in PLAYERS])
	active_player = [player for player in PLAYERS if player.is_active][0]
	print("Players info:", players_info)

	response_format = '{"action": "Assassinate", "target": "PlayerB", "explanation: "some explanation here"}'
	completion = client.chat.completions.create(
		model="gpt-4-1106-preview",
		response_format={"type": "json_object"},
		messages=[
			{"role": "system", "content": f"I play COUP card game. The game state is as follows {players_info}"},
			{"role": "user", "content": f"""Tell me best next move for active player. 
																	Give response in JSON including short explanation in format {response_format}"""}
  	]
	)
	response_message = completion.choices[0].message.content
	prompt_response = PromptResponse(**json.loads(response_message))
	response_parser.parse_model(active_player.nick, prompt_response)

	print("Prompt response:", prompt_response)	
	print("----------------------------")


def __get_player_info(player: Player):
	player_chose = {}
	card_claim = {}
	player_info = player.describe()

	for log in GAME_LOGS:
		parsed_log = __get_parsed_log(log)
		if parsed_log.player == player.nick:
			if parsed_log.action == 'chose':
				player_chose[parsed_log.value] = player_chose.get(parsed_log.value, 0) + 1
			if parsed_log.action == 'claim':
				card_claim[parsed_log.value] = card_claim.get(parsed_log.value, 0) + 1

	player_choose_info = __get_activity_info("chose", player_chose)
	if player_choose_info != "":
		player_info += f", {player_choose_info}"

	card_claim_info = __get_activity_info("claim", card_claim)
	if card_claim_info != "":
		player_info  += f", {card_claim_info}"

	return player_info


def __get_activity_info(activity_key: str, info: dict):
	return ", ".join([f"{activity_key} {k} {v} times" for k,v in info.items()])


def __get_parsed_log(log: str) -> GameLog:
  data = log.split(" ")
  return GameLog(
		player=data[0], 
		action=data[1], 
		value=data[2] if len(data) == 3 else None
	)