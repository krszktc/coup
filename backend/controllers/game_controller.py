from fastapi import APIRouter
from models.game_model import Game
from models.user import UserDto
from services import game_service

router = APIRouter(
    prefix="/game",
    tags=["game"],
)

@router.post("/create")
async def create_game(user: UserDto) -> Game:
    return game_service.create_game(user.id)


@router.post("/add/{game_id}")
async def add_player(game_id: str, user: UserDto) -> Game:
    return game_service.add_player_to_game(game_id, user.id)


@router.post("/start/{game_id}")
async def start_game(game_id: str, user: UserDto) -> Game:
    return game_service.start_game(game_id, user.id)


@router.get("/status/{game_id}")
async def check_game_status(game_id: str) -> Game:
    return game_service.get_game(game_id)





