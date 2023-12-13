from fastapi import FastAPI
from pydantic import BaseModel
import chat_service_b as chat_service

app = FastAPI()


class MockContent(BaseModel):
    messages: list[str]


@app.post("/mock/str")
def mock_server_state(mock_data: MockContent):
    chat_service.mock_string_progress(mock_data.messages)
    return {"state": "OK"}


@app.post("/mock/json")
def mock_server_state(mock_data: MockContent):
    chat_service.mock_json_process(mock_data.messages)
    return {"state": "OK"}