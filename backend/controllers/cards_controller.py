from fastapi import APIRouter
from models.card import Card
from services import card_service

router = APIRouter(
    prefix="/cards",
    tags=["cards"],
)

@router.get("/")
async def get_all_cards() -> list[Card]:
  return card_service.get_all()