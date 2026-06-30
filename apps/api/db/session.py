from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.config import settings

# The engine is the connection pool — it manages multiple connections to Postgres.
# pool_pre_ping=True tests the connection before using it, avoiding stale connections.
engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
    echo=settings.environment == "development",
)

# Session factory — each request gets its own session from this factory.
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that provides a database session per request."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
