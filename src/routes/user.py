from fastapi import APIRouter, Response, status, HTTPException, Depends
from src.db import conn
from src.middleware import get_db
from src.models import users
from src.schemas import User
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT
from starlette.status import HTTP_404_NOT_FOUND

from typing import List

from sqlalchemy.sql.expression import select

user = APIRouter()

@user.get('/users', response_model=list[User], tags=['users'])
def get_users(db: Session = Depends(get_db)):
    return db.execute(users.select()).fetchall()

@user.get('/users/{sha_dni}', response_model=User, tags=['users'])
def get_user(sha_dni: str, db: Session = Depends(get_db)):
    user = db.execute(users.select().where(users.c.sha_dni == sha_dni)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user.post('/users', response_model=User, tags=['users'])
def create_user(user: User, db: Session = Depends(get_db)):
    new_user = {'sha_dni': user.sha_dni, 'voto': False, 'lugar_residencia': user.lugar_residencia}
    try:
        result = db.execute(users.insert().values(new_user))
        created_user_id = result.inserted_primary_key[0]
        new_user["id"] = created_user_id # Agregar el ID generado a la respuesta
        return new_user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=f"Error creating user: {e}")

@user.put('/users/{sha_dni}', response_model=User, tags=['users'])
def update_user(sha_dni: str, db: Session = Depends(get_db)):
    user = db.execute(users.select().where(users.c.sha_dni == sha_dni)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.voto:
        return db.execute(users.select().where(users.c.sha_dni == sha_dni)).first()

    try:
        db.execute(users.update().values(voto=True).where(users.c.sha_dni == sha_dni))
        return db.execute(users.select().where(users.c.sha_dni == sha_dni)).first()
    except SQLAlchemyError:
        raise HTTPException(status_code=400, detail="Error updating user")

@user.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['users'])
def delete_user(id: str, db: Session = Depends(get_db)):
    db.execute(users.delete().where(users.c.id == id))
    return Response(status_code=HTTP_204_NO_CONTENT)