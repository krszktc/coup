from fastapi import FastAPI
from pydantic import BaseModel
import chat_service_c as chat_service

app = FastAPI()


@app.post("/mock")
def mock_server_state():
    chat_service.mock_progress()
    return {"state": "OK"}
