from pydantic import BaseModel

class User(BaseModel):
    id: int
    sha_dni: int
    voto: bool
    lugar_residencia: str