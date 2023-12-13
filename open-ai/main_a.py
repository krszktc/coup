from fastapi import FastAPI
from pydantic import BaseModel
import chat_service_a as chat_service

app = FastAPI()


class MockContent(BaseModel):
    messages: list[str]


@app.post("/game/new")
def new_game():
    chat_service.game_new()
    return {"state": "OK"}


@app.post("/game/end")
def end_game():
    chat_service.game_end()
    return {"state": "OK"}


@app.post("/mock")
def mock_server_state(mock_data: MockContent):
    chat_service.set_mock_state(mock_data)
    return {"state": "OK"}


@app.get("/state")
def get_game_state():
    return chat_service.get_game_messages()