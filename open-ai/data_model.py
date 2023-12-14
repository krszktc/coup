from pydantic import BaseModel


class PromptResponse(BaseModel):
	action: str
	target: str
	explanation: str


class GameLog(BaseModel):
	player: str
	action: str
	value: str | None


class Card(BaseModel):
	character_name: str
	visible_for_others: bool = False


class Player(BaseModel):
	nick: str 
	coins: int = 0
	cards: list[Card] = []
	is_active: bool = False
	claim: str | None = None


	def describe(this):
		card_1 = this.cards[0]
		card_2 = this.cards[1]
		if (not card_1.visible_for_others) or (not card_2.visible_for_others):
			card_1_visibility = this.__describe_card(card_1)
			card_2_visibility = this.__describe_card(card_2)
			base_info = f"{this.nick} is active player," if this.is_active else this.nick
			return f"{base_info} has one card {card_1_visibility}, second card {card_2_visibility} and {this.coins} coins"
		return f"{this.nick} is out"
	

	def __describe_card(this, card: Card):
		visibility = "visible" if card.visible_for_others else "hide"
		if this.is_active or card.visible_for_others:
			return f"{card.character_name} {visibility}"
		return visibility


# Take from db after init request for AI to play in the game
GAME_LOGS = [
	"PlayerA turn",
	"PlayerA claim Income",
	"PlayerA effect take_1_coin",
	"PlayerB turn",
	"PlayerB claim Duke",
	"PlayerA pass",
	"PlayerC pass",
	"PlayerC effect take_3_coins",
	"PlayerC turn",
	"PlayerC claim ForeignAid",
	"PlayerA claim Duke",
	"PlayerC challenge",
	"PlayerC loosed challenge",
	"PlayerC choose card",
	"PlayerC chose Ambassador",
	"PlayerC loosed power",
	"PlayerA turn",
]
PLAYERS = [
	Player(
		is_active= True,
		nick= "PlayerA",
		claim= "Duke",
		coins= 3,
		cards= [ 
			Card(character_name="Duke"),
			Card(character_name="Captain")
		]
	),
	Player(
		nick= "PlayerB",
		claim= None,
		coins= 5,
		cards= [ 
			Card(character_name="Assassin"), 
			Card(character_name="Duke") 
		]
	),
		Player(
		nick= "PlayerC",
		claim= None,
		coins= 2,
		cards= [ 
			Card(character_name="Contessa"), 
			Card(character_name="Ambassador", visible_for_others=True) 
		]
	)
]
GAME_ACTIONS = ["Income", "Foreign Aid", "Coup", "Tax", "Assassinate", "Exchange", "Steal", "Block Assassination"]
GAME_CARDS = ["Duke", "Assassin", "Ambassador", "Captain", "Contessa"]
PLAYER_NICKS = [player.nick for player in PLAYERS]
