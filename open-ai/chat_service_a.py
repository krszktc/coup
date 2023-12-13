from openai import OpenAI
import response_parser

client = OpenAI()

# Statefull service AntiPattern, don't do this on prod!!!
# Thread represent Game
state = {
	"thread": None,
	"playerB": None,
	"playerC": None,
	"runB": None,
	"runC": None
}


# https://platform.openai.com/docs/api-reference/threads
# "Create threads that ASSISTANTS can interact with" <------------------------------------------- inconsistency
# {
# 	'error': {
# 		'message': 'Thread thread_9voLadIpduDEqAdSWfJAeNEL already has an active run run_ZQhN8IOL7ucG0mVixnKzmm6P.', 
# 		'type': 'invalid_request_error', 
# 		'param': None, 
# 		'code': None
# 		}
# }
def game_new():
	state["thread"] = client.beta.threads.create()
	state["playerB"] = __create_agent("PlayerB", "Duke", "Duke")
	state["playerC"] = __create_agent("PlayerC", "Ambassador", "Assassin")
	state["runB"] = __run_create(state["playerB"].id)
	state["runC"] = __run_create(state["playerC"].id)
	print(f"State set: {state}")
	

def game_end():
	client.beta.assistants.delete(state["playerB"].id)
	client.beta.assistants.delete(state["playerC"].id)
	client.beta.threads.runs.cancel(state["thread"].id, state["runB"].id)
	client.beta.threads.runs.cancel(state["thread"].id, state["runC"].id)
	client.beta.threads.delete(state["thread"].id)
	print("Game removed")


def set_mock_state(mock_messages: list[str]):
	for message in mock_messages:
		client.beta.threads.messages.create(
			thread_id=state["thread"].id,
			content=message,
			role="user"
		)
	messages = client.beta.threads.messages.list(
		thread_id=state["thread"].id
	)
	message_values = [message.content[0].text.value for message in messages]
	print(f"All messages: {message_values}")


def get_game_messages():
	messages = client.beta.threads.messages.list(
		thread_id=state["thread"].id
	)
	messages = [message.content[0].text.value for message in messages]
	response_parser.parse(messages[-1])
	return messages


def __create_agent(name: str, firstCard: str, secondCard: str) -> str:
	assistant = client.beta.assistants.create(
		name=name,
		instructions=f"We play COUP card game. You are {name}. You have hidden {firstCard} card, hidden {secondCard} card and 2 coins",
		tools=[{"type": "code_interpreter"}],
		model="gpt-4-1106-preview"
		# model="ft:gpt-3.5-turbo-1106:hops::8UyaBRkC" <--- doesn't work with Assistants
	)
	print(f"Assistant {name}: {assistant}")
	return assistant


def __run_create(assistant_id: str):
	run = client.beta.threads.runs.create(
		thread_id=state["thread"].id,
		assistant_id=assistant_id
	)	
	print(f"New run: {run}")
	return run