from fastapi import APIRouter, Depends, HTTPException, status
from app.router.dependencies import get_current_user
from app.schemas.usuarios import CrearUsaurio, EditarUsuario, EditarPass, RetornarUsuario
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from core.database import get_db # funcion que fabrica funciones en database.py
from app.crud import usuarios as crud_users # se pone un alias, para evitar equivocacion, ya que existen varios archivos con el nombre usuarios.

router = APIRouter() # creando objeto router de la clase APIRouter()

#ruta insertar usuario
@router.post("/registrar", status_code=status.HTTP_201_CREATED) # cuando hay una @ y luego una funcion se llama un decorador y es agregarle superpoderes a rutas, se esta creando una api con esta linea de código y la ruta se pone como decorador de la funcion. status_code=status.HTTP_201_CREATED devuelve un código de status  en esta caso 201 que significa que todo salio bien
def create_user(
    user: CrearUsaurio,
    db: Session = Depends(get_db), #Depends funciona como una condición para que continue la ejecución, en este caso se condiciona a que continue la funcion create_user a que esté get_db
    user_token: RetornarUsuario = Depends(get_current_user) # linea o argumento que pide la funcion para proteger el endpoint
): 
    try:
        if user_token.id_rol != 1:# condicion para controlar el tipo de usuario que puede crear usuarios
            raise HTTPException(status_code=401, detail="No tienes permisos")
        crud_users.create_user(db, user)
        return {"message": "Usuario creado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#ruta consultar usuario por id
@router.get("/obtener-por-id/{id_usuario}", status_code=status.HTTP_200_OK, response_model=RetornarUsuario) # se debe colocar que nos arroja la funcion siguiente
def get_by_id(
    id_usuario:int , 
    db:  Session = Depends(get_db),
    user_token: RetornarUsuario = Depends(get_current_user)
):
    try:
        user = crud_users.get_user_by_id(db, id_usuario)
        
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        
        return user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


#ruta consultar usuario por correo
@router.get("/obtener-por-correo/{correo}", status_code=status.HTTP_200_OK, response_model=RetornarUsuario) # se debe colocar que nos arroja la funcion siguiente
def get_by_email(
    correo:str, 
    db:  Session = Depends(get_db),
    user_token: RetornarUsuario = Depends(get_current_user)
):
    try:
        user = crud_users.get_user_by_email(db, correo)
        
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        
        return user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

#ruta editar usuario
@router.put("/editar/{user_id}")
def update_user(
    user_id: int, 
    user: EditarUsuario, 
    db: Session = Depends(get_db),
    user_token: RetornarUsuario = Depends(get_current_user)
):
    try:       
        success = crud_users.update_user(db, user_id, user)
        if not success: # se condiciona si no es satisfactorio o llego información
            raise HTTPException(status_code=400, detail="No se pudo actualizar el usuario")
        return {"message": "Usuario actualizado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

#ruta editar contraseña por id
# @router.put("/editar-contrasenia")
# def update_password(user: EditarPass, db: Session = Depends(get_db)):
#     try:
#         # aqui se busca verificar si la contraseña anterior es igual a la almacenada en la base de datos y manda mensaje 
#         verificar = crud_users.verify_user_pass(db, user)
#         if not verificar:
#             raise HTTPException(status_code=400, detail="La contraseña actual no es igual a la enviada")
        
#         success = crud_users.update_password(db, user)
#         if not success:# se condiciona si no es satisfactorio o llego información
#             raise HTTPException(status_code=400, detail="No se pudo actualizar la contraseña del usuario")
#         return {"message": "Contraseña actualizada correctamente"}
#     except SQLAlchemyError as e:
#         raise HTTPException(status_code=500, detail=str(e))


@router.put("/editar-contrasenia")
def update_password(
    user: EditarPass, 
    db: Session = Depends(get_db),
    user_token: RetornarUsuario = Depends(get_current_user)
):
    try:
        verificar = crud_users.verify_user_pass(db, user)
        if not verificar:
            raise HTTPException(status_code=400, detail="La contraseña actual no es igual a la enviada")

        success = crud_users.update_password(db, user)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar la contraseña del usuario")
        return {"message": "Contraseña actualizada correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


#ruta eliminar usuario por id
@router.delete("/eliminar-por-id/{id_usuario}", status_code=status.HTTP_200_OK)
def delete_by_id(
    id_usuario:int, 
    db:  Session = Depends(get_db),
    user_token: RetornarUsuario = Depends(get_current_user)
):
    try:
        user = crud_users.user_delete(db, id_usuario)
        if user:
            return {"message": "Usuario eliminado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))