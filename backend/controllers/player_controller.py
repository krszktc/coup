from fastapi import APIRouter
from models.player_model import PlayerActionDto
from services import player_service
from models.game_model import GameDto, ActionDto

router = APIRouter(
    prefix="/player",
    tags=["player"],
)

@router.post("/action/{card_code}")
async def action(card_code: str, dto: ActionDto) -> PlayerActionDto:
    operation = player_service.action(card_code, dto)
    return PlayerActionDto(operation)


@router.post("/card/{card_code}")
async def card(dto: GameDto) -> PlayerActionDto:
    operation = player_service.card(dto)
    return PlayerActionDto(operation)


@router.post("/pass")
async def decision_pass(dto: GameDto) -> PlayerActionDto:
    operation = player_service.decision_pass(dto)
    return PlayerActionDto(operation)


@router.post("/challenge")
async def decision_challenge(dto: GameDto) -> PlayerActionDto:
    operation = player_service.decision_challenge(dto)
    return PlayerActionDto(operation)
