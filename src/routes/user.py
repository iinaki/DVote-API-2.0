
from fastapi import APIRouter, Response, status
from src.db import conn
from src.models import users
from src.schemas import User
from starlette.status import HTTP_204_NO_CONTENT

user = APIRouter()

@user.get('/users', response_model=list[User], tags=['users'])
def get_users():
    return conn.execute(users.select()).fetchall()

@user.get('/users/{sha_dni}', response_model= User, tags=['users'])
def get_user(sha_dni: str):
    return conn.execute(users.select().where(users.c.sha_dni == sha_dni)).first()

@user.post('/users', response_model=User, tags=['users'])
def create_user(user: User):
    new_user = {'id': user.id, 'sha_dni': user.sha_dni, 'voto': user.voto, 'lugar_residencia': user.lugar_residencia}
    result = conn.execute(users.insert().values(new_user))
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()

@user.put('/users/{sha_dni}', response_model=User, tags=['users'])
def update_user(sha_dni: str):
    user = conn.execute(users.select().where(users.c.sha_dni == sha_dni)).first()
    if not user:
        return {'msg': 'User not found'}
    
    if user.voto == True:
        return {'msg': 'User already voted'}

    conn.execute(users.update().values(voto=True).where(users.c.sha_dni == sha_dni))
    return conn.execute(users.select().where(users.c.sha_dni == sha_dni)).first()

@user.delete('/users/{id}', status_code= status.HTTP_204_NO_CONTENT, tags=['users'])
def delete_user(id: str):
    result = conn.execute(users.delete().where(users.c.id == id)).first()
    return Response(status_code=HTTP_204_NO_CONTENT)