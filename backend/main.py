from fastapi.responses import JSONResponse
from controllers import game_controller, player_controller, cards_controller
from fastapi import FastAPI, Request
from models.exceptions.exceptions import InfoException, DataModelException

app = FastAPI()
app.include_router(game_controller.router)
app.include_router(cards_controller.router)
app.include_router(player_controller.router)


@app.exception_handler(InfoException)
async def info_exception_handler(request: Request, exc: InfoException):
    return JSONResponse(
        status_code=400,
        content={ "error": exc.message },
    )


@app.exception_handler(DataModelException)
async def info_exception_handler(request: Request, exc: DataModelException):
    return JSONResponse(
        status_code=422,
        content={ "error": exc.message },
    )