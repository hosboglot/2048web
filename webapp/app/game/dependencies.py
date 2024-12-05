from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.session_maker import SessionDep, session_manager

from app.game.game import GameServer
from app.game.dao import GameDAO


active_games: dict[int, GameServer] = {}


async def get_game_server(game_id: int):
    async with session_manager.create_session() as session:
        game = await GameDAO.find_one_or_none_by_id(game_id, session)
    if not game:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'No game found with id {game_id}')
    server = active_games.get(game_id)
    if not server:
        server = GameServer(game_id)
        active_games[game_id] = server
    return server
