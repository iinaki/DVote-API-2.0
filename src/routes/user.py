
from fastapi import APIRouter, Response, status, HTTPException
from src.db import conn
from src.models import users
from src.schemas import User
from sqlalchemy.exc import SQLAlchemyError

user = APIRouter()

@user.get('/users', response_model=list[User], tags=['users'])
def get_users():
    return conn.execute(users.select()).fetchall()

@user.get('/users/{sha_dni}', response_model=User, tags=['users'])
def get_user(sha_dni: str):
    user = conn.execute(users.select().where(users.c.sha_dni == sha_dni)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user.post('/users', response_model=User, tags=['users'])
def create_user(user: User):
    new_user = {'sha_dni': user.sha_dni, 'voto': False, 'lugar_residencia': user.lugar_residencia}
    try:
        result = conn.execute(users.insert().values(new_user))
        new_user['id'] = result.lastrowid
        return new_user
    except SQLAlchemyError:
        raise HTTPException(status_code=400, detail="Error creating user")

@user.put('/users/{sha_dni}', response_model=User, tags=['users'])
def update_user(sha_dni: str):
    user = conn.execute(users.select().where(users.c.sha_dni == sha_dni)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.voto:
        raise HTTPException(status_code=400, detail="User already voted")

    try:
        conn.execute(users.update().values(voto=True).where(users.c.sha_dni == sha_dni))
        return conn.execute(users.select().where(users.c.sha_dni == sha_dni)).first()
    except SQLAlchemyError:
        raise HTTPException(status_code=400, detail="Error updating user")

@user.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['users'])
def delete_user(id: str):
    conn.execute(users.delete().where(users.c.id == id))
    return Response(status_code=HTTP_204_NO_CONTENT)