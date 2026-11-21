from collections.abc import AsyncIterator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from interactive_video_backend_core.storage import AbstractSessionRepository
from interactive_video_backend_core.storage_sqlalchemy import SQLAlchemySessionRepository


async def get_repository(
    request: Request,
) -> AsyncIterator[AbstractSessionRepository]:
    session_factory: async_sessionmaker[AsyncSession] = request.app.state.session_factory
    async with session_factory() as session:
        yield SQLAlchemySessionRepository(session)
