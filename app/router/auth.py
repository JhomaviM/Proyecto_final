from typing import Annotated
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.router.dependencies import authenticate_user
from app.schemas.auth import ResponseLoggin
from core.security import create_access_token
from core.database import get_db
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()

@router.post("/token", response_model=ResponseLoggin)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], #form_data recibe el username y password de la libreria OAuth2PasswordRequestForm, esta libreria no se usa solo en python, se puede usar en otros lenguajes, esta libreria es como un esquema muy bien validado
    db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db) # regresa un bool
    if not user: # verifica si user no es verdadero
        raise HTTPException(
            status_code=401,
            detail="Datos Incorrectos en email o password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": str(user.id_usuario), "rol":user.id_rol}
    )

    return ResponseLoggin(
        user=user,
        access_token=access_token
    )