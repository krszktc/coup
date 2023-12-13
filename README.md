# Info

Simple COUP game implementation proposal.

More detailed rules description could be found here:\
`https://www.ultraboardgames.com/coup/game-rules.php`

## backend
Python FastApi game server. To run it call `uvicorn main:app` in `/backend` folder\
The API is available under `http://localhost:8000/docs`

## ai
Simple AI client which can act as regular player calling the same API endpoints.\
To run the client call `uvicorn main:app` in `/ai` folder

## ui
React API client. To run it call `npm start` in `/ui` folder \
The page is available under `http://localhost:4000`

## open-ai
Fast api ChatGPT client. TO run it update `OPENAI_API_KEY` in `.env` file and run `uvicorn main_b:app --env-file .env`. The `main_a.py` contain issued implementation leaved only for review purpose.
 
# Description

The game run as intended in the description provided above. The players take runs trying to reduce influence other players by discover their cards.

Technically it looks like following.

Each user can be part of different games being wrapped by Player model. So different instances of player which are part of different games contain reference to the same user. User can be referenced in number of different Players, but Player can be part only one game. 

The Game can contain number of players. Each player can be human or AI. AI players are create in the same process as human player but one extra request is send to AI server, to store player id which will be supervised by AI agent. This approach allow AI to easily replaceable by any other system or running in parallel. Also in allow Real player for example to be advice by the AI about next move, base of Player state but final decision can be take by the player. 

UI act as standalone client. Any other way of use API (postman, curl, API doc page) is allowed to play the game. The dashboard present sub-space for each player and full list of cards for speculations. Players can submit 4 type of actions: 
- `card` to report "action", "contraction" or point "power loose"
- `action` special version of `card` contain target player
- `challenge` to check if ActionPlayer or ContractionPlayer really has claimed card
- `pass` which is opposite action fro challenge and contraction

Game contain number of states, represent by `GameStatus`. On each state, submitted actions has different context and turn out to execute different Game checks.

The AI model should be trained base of play sessions between real players. Logs model has been designed to be minimalistic. Thanks to that ChatGPT use smaller number of tokens to generate response and more easy to parse content.

# Structure

Responsibility and short description for specific files

## backend
The service contain a few controllers to manage `cards`, `game`, and `players`. The controllers are loaded in `main.py` during server start. Main file contain also exception handler to error defined in `/model/exceptions`. Thanks to this each typed error thrown from application is catch and converted to declared api response.

Models use `pydantic` class definition extended by methods to self-state management. There is no encapsulation used to exclude necessary to have setter for each private private property. Going this way the models has limited self-state-management functionality and most of the manipulations are made by services.

The application use fake-persistence which is in-memory collection of date, reset after each server restart. In case of use real db repository should stay in more or less similar form and extra query layer should be adder after it. 

## ai
Should work asa separate service/microservice but in very small application like this one could be part of `backend` and use the same db. The service use only one controller to store list of games and related players for which action need to be called. Cron scheduler in `cron_game.py` fire up the verification process each 10 second. `request_service.py` call `backend` api to get game status. Base of information received `game_service.py` decide what kind of action need to be taken and what kind of request submit.

This part contain doubled model with backend but monorepo could be used instead to share models across the service

## ui
Contain a few small components represent accordingly `card`, `player board` and `game board`. Current state contain mock data and is not integrated neither with backend nor Ai service. `request.service.ts` contain list of functions to get data. React with TypeScript hs been used. 

## open-ai
Contain two FastApi applications. First one `main_a.py` has broken implementation for multiple Assistants working in parallel on the same Thread. It doesn't work correctly by it experimental character. Second one `main_b.py` contain classic approach with chat completion. `chat_service_a.py` and `chat_service_b.py` are related to applications.

The flow for `main_b` contain replaceable controllers operate on string and json responses. The controllers could be used alternately on any step of game.

Folder `files` contain scenarios to train ChatGPT model in readable format as `coup_learn.jsonl` and parseable format as `coupe_learn_single_line.py`. The model return some inconsistent responses from time to time but only 12 examples has been used in fine-tunning. File `example_flow.png` shows example game session with ChatGPT play as PlayerB and PlayerC

# ToDo
- finish UI (currently more like backbone)
- finish AI (currently more like backbone)
- integration (real API calls)
- test scenarios


# Demo Improvements
- reduce game model, keep state in iterator
- split `card` to two controllers
- add time lock to resolve specific step in case of lack user reaction
- serve UI static files
- logs storage


# Prod Improvements
- real db
- cache
- add third service as kind of gateway between backend call and AI agents run
- queue AI agents checking