from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import aiomysql
from fastapi import HTTPException

DB_CONFIG = "mysql+aiomysql://feras:Feras12345321@10.13.0.230/NMv2"

class AsyncDatabaseSession:
    def __init__(self):
        self.session = None
        self.engine = None

    def __getattr__(self,name):
        return getattr(self.session,name)
    
    def init(self):
        self.engine = create_async_engine(DB_CONFIG,future=True,echo=True)
        self.session= sessionmaker(self.engine,expire_on_commit=False,class_=AsyncSession)()

    async def create_all(self):
        async with self.engine.begin() as con:
            await con.run_sync(SQLModel.metadata.create_all)

db = AsyncDatabaseSession()

async def commit_rollback():
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise

