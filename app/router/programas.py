from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from app.schemas.programas import ProgramaBase
from utils.utils import save_uploaded_document
from app.crud.programas import get_programa_by_cod, update_url_pdf
from core.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.crud import programas as crud_programas
from app.router.dependencies import get_current_user


router = APIRouter(
    prefix="/programas",
    tags=["Documentos"]
)

@router.post("/subir-pdf/")
def upload_document(
    codigo: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Sube un archivo PDF, Word o Excel al servidor y devuelve su ruta de almacenamiento.
    """
    try:
        # filtro que busca programa
        programa = get_programa_by_cod(db, codigo)
        
        if programa is None:
            raise HTTPException(status_code=404, detail="El progama no existe en la base de datos")
        
        file_path = save_uploaded_document(file)
       
        
        save_url = update_url_pdf(db, codigo, file_path)
        
        return {
            "message": "Archivo subido correctamente",
            "filename": file.filename,
            "ruta_servidor": file_path
        }
    except HTTPException as e:
        # Retorna los errores personalizados definidos en la función
        raise e
    except Exception as e:
        # Captura cualquier otro error inesperado
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/obtener-todos-programas", status_code=status.HTTP_200_OK, response_model=List[ProgramaBase])
def get_all(db: Session = Depends(get_db)):
    try:
        programas = crud_programas.get_all_programas(db)
        if programas is None:
            raise HTTPException(status_code=404, detail="Programas no encontrados")
        return programas
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# @router.get("/obtener-todos-programas-secure", status_code=status.HTTP_200_OK, response_model=List[ProgramaBase])
# def get_all_s(
#     db: Session = Depends(get_db),
#     user_token: ProgramaBase = Depends(get_current_user)
# ):
#     try:
#         if user_token.id_rol != 1:
#             raise HTTPException(status_code=401, detail="No tienes permisos para crear usuario")
        
#         programas = crud_programas.get_all_user(db)
#         if programas is None:
#             raise HTTPException(status_code=404, detail="Usuarios no encontrados")
#         return programas
#     except SQLAlchemyError as e:
#         raise HTTPException(status_code=500, detail=str(e))
