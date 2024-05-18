from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, Boolean 
from src.db import meta, engine

users = Table(
    'user', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('sha_dni', BigInteger),
    Column('voto', Boolean),
    Column('lugar_residencia', String(255))
)

meta.create_all(bind=engine)
