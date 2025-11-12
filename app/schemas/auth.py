from pydantic import BaseModel
from app.schemas.usuarios import RetornarUsuario


class ResponseLoggin(BaseModel):
    user: RetornarUsuario
    access_token: str