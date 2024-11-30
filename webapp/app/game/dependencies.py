from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.session_maker import SessionDep

from app.game.game import GameServer


active_games: dict[int, GameServer] = {}

def get_game_server(game_id: int):
    server = active_games.get(game_id)
    if not server:
        server = GameServer()
        active_games[game_id] = server
    return server
