from enum import Enum
from typing import AsyncGenerator, Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from .config import settings


engine = create_async_engine(settings.DATABASE_URL_ONE, echo=True)
engine2 = create_engine(settings.DATABASE_URL_ONE, echo=True)

AsyncSessionFactory = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
SyncSessionFatory = sessionmaker(bind=engine2, class_=Session, expire_on_commit=False)

class SessionClass(str, Enum):
    async_class = "async_class"
    sync_class = "sync_class"
    
def make_session(session_type: SessionClass):
    if session_type == SessionClass.async_class:
        return AsyncSessionFactory()
    elif session_type == SessionClass.sync_class:
        return SyncSessionFatory()
    else: 
        raise ValueError("Invalid session type")
        
        
async def get_async_db() -> AsyncGenerator:
    async with make_session(SessionClass.async_class) as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

            
def get_sync_db() -> Generator:
    with make_session(SessionClass.sync_class) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
            