from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[int]
    sha_dni: str
    voto: bool
    lugar_residencia: str

    class Config:
        orm_mode = True