from collections.abc import AsyncGenerator
import uuid

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime


DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Creating data models
# We use "declarative_base" to create a base class that our models will inherit from.
# This base class will be used to define the structure of our database tables.

# Creating base class for our models because directly using DeclarativeBase will not work
class Base(DeclarativeBase):
    pass

# The columns in a table map directly to fields in a model class.
# We use "Base" instead of "DeclarativeBase"
class Post(Base):
    __tablename__ = "posts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caption = Column(String(255))
    url = Column(String(255), nullable=False)
    file_type = Column(String(255), nullable=False)
    file_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Creating database engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to True for SQL query logging
    future=True # Set to True for SQLAlchemy 2.0 style (recommended)
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession, # Pass the async session class
    expire_on_commit=False, # Set to False for automatic commits
    autoflush=False, # Set to False to prevent automatic flushing
)

async def create_db_and_tables():
    async with engine.begin() as conn:
        # await conn.run_sync() is used to run synchronous code in an async context
        # DeclarativeBase.metadata is a collection of all tables
        # .create_all() creates all tables defined in the models
        await conn.run_sync(Base.metadata.create_all)

# Dependency Injection Function
# This function will be used to get a session for each request
# It will automatically open and close the session
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()