from fastapi import APIRouter, Response, Depends, WebSocket, websockets
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.auth.dependencies import get_current_user, get_current_admin_user
from app.auth.models import User
from app.auth.auth import authenticate_user, create_access_token

from app.game.game import GameServer
from app.game.models import Game
from app.game.dao import GameDAO
from app.game.schemas import SGameCreate, SGameCreateDB
from app.game.dependencies import get_game_server

from app.dao.session_maker import TransactionSessionDep, SessionDep

router = APIRouter(prefix='/game', tags=['Auth'])


@router.post("/create")
async def create_game(
        game: SGameCreate,
        user: User = Depends(get_current_user),
        session: AsyncSession = TransactionSessionDep):
    new_game: Game = await GameDAO.add(session=session, values=SGameCreateDB(**game.model_dump(), host_id=user.id))
    logger.info(f"Создана игра с ID {new_game.id}")
    return {'message': 'Игра создана'}


@router.websocket("/{game_id}")
async def enter_game(
        websocket: WebSocket,
        server: GameServer = Depends(get_game_server),
        user: User = Depends(get_current_user)):
    await server.connect_player(user.id, websocket)
    try:
        await server.play(user.id)
    except websockets.WebSocketDisconnect:
        logger.info(f"Player {user.id} disconnected from game {server._game_id}")
        await server.disconnect_player(user.id)
