from fastapi import APIRouter
from models.player_model import PlayerActionDto
from services import player_service
from models.game_model import GameDto

router = APIRouter(
    prefix="/player",
    tags=["player"],
)

@router.post("/card/{card_code}")
async def raise_card(card_code: str, dto: GameDto) -> PlayerActionDto:
    operation = player_service.raise_card(card_code, dto)
    return PlayerActionDto(operation)


@router.post("/pass")
async def decision_pass(dto: GameDto) -> PlayerActionDto:
    operation = player_service.decision_pass(dto)
    return PlayerActionDto(operation)


@router.post("/challenge")
async def decision_challenge(dto: GameDto) -> PlayerActionDto:
    operation = player_service.challenge(dto)
    return PlayerActionDto(operation)
