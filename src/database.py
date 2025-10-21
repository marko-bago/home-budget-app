from src.config import settings
from sqlalchemy.engine.url import make_url

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine
)

from sqlalchemy.orm import DeclarativeBase

def create_db_engine(connection_string: str):
    """Create a database engine with proper timeout settings.

    Args:
        connection_string: Database connection string
    """
    url = make_url(connection_string)

    # Use existing configuration values with fallbacks
    timeout_kwargs = {
        # Connection timeout - how long to wait for a connection from the pool
        "pool_timeout": settings.DATABASE_ENGINE_POOL_TIMEOUT,
        # Recycle connections after this many seconds
        "pool_recycle": settings.DATABASE_ENGINE_POOL_RECYCLE,
        # Maximum number of connections to keep in the pool
        "pool_size": settings.DATABASE_ENGINE_POOL_SIZE,
        # Maximum overflow connections allowed beyond pool_size
        "max_overflow": settings.DATABASE_ENGINE_MAX_OVERFLOW,
        # Connection pre-ping to verify connection is still alive
        "pool_pre_ping": settings.DATABASE_ENGINE_POOL_PING,
    }
    return create_async_engine(url, future=True, echo=True, **timeout_kwargs)


# Create the default engine with standard timeout
engine = create_db_engine(settings.SQLALCHEMY_DATABASE_URI)

SessionFactory = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    __repr_attrs__ = []
    __repr_max_length__ = 20


    def as_dict(self):
        """Returns a dict representation of a model."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    

