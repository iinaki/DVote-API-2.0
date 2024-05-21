from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData


DATABASE_URL = "postgresql://dvote_user:aD7nniFvRBRiCc4rkSTBWcypCQh18yka@dpg-cp0nkta1hbls73edkjc0-a.ohio-postgres.render.com/dvote"

# class Base(DeclarativeBase):
#     pass

# engine = create_engine(url=DATABASE_URL, echo=True)
engine = create_engine(url=DATABASE_URL)
meta = MetaData()
conn = engine.connect()    

# async def get_session():
#     async_session = async_sessionmaker(bind=engine, expire_on_commit=False) 
#     yield async_session

# async def init_db():
#     async with engine.begin() as conn:
#         from src.models import User
#         await conn.run_sync(Base.metadata.create_all)