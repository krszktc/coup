from fastapi import FastAPI
from services import game_service, request_service

app = FastAPI()

game_service.save_game(request_service.get_cards())

@app.post("/supervise/{game_id}/{user_id}")
def supervise(game_id: str, user_id: str):
    game_service.save_game(game_id, user_id)