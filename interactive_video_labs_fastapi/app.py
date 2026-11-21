from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from interactive_video_backend_core.orm_models import Base
from interactive_video_backend_core.models import SessionResumeResponse

from .routes import resume_session, save_decision, validate_transition


def create_app(
    database_url: str = "sqlite+aiosqlite:///./interactive_video.db",
) -> FastAPI:
    engine: AsyncEngine = create_async_engine(database_url)
    session_factory = async_sessionmaker(engine, class_=AsyncSession)
    app = FastAPI(
        title="interactive-video-labs-fastapi",
        version="0.2.0",
    )
    app.state.session_factory = session_factory

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        yield
        await engine.dispose()

    app.router.lifespan_context = lifespan
    app.add_api_route(
        "/decisions",
        save_decision,
        methods=["POST"],
        status_code=201,
    )
    app.add_api_route(
        "/sessions/{user_id}/{session_id}",
        resume_session,
        methods=["GET"],
        response_model=SessionResumeResponse | None,
    )
    app.add_api_route(
        "/transitions/validate",
        validate_transition,
        methods=["POST"],
    )

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app
