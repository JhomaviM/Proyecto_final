from fastapi import HTTPException, status
from sqlalchemy.orm import Session # para trabajar con sesiones
from sqlalchemy import text # limpia el sql de posibles ataques de inyecion sql
from sqlalchemy.exc import SQLAlchemyError # se utiliza para el manejo de errores
from typing import Optional
import logging

from app.schemas.usuarios import CrearUsaurio, EditarUsuario, EditarPass # importamos los schemas creados en el archivo schemas
from core.security import get_hashed_password, verify_password  # importamos las funciones para encriptar y verificar una password

logger = logging.getLogger(__name__) # Sirve para registrar errores del sistema

# funcion que realiza insert a la base de datos , utilizando orden, control de errores y validacion de datos, con seguridad informatica
def create_user(db: Session, user: CrearUsaurio) -> Optional[bool]:
    try: # quiere decir que se haga esto, pero si surge un error o falla entonces vaya por el except, sirve para controlar errores o fallas cuando surjan
        dataUser = user.model_dump() # convierte el esquema en diccionario y lo guarda en la variable, # model_dump() todo lo que tiene guardado user lo convierte en json
        contraOrigin = dataUser["contra_encript"] # saca la contra original
        contraEncript = get_hashed_password(contraOrigin) # envia la contraOriginal a encriptar y la guarda en la variable contraEncript
        dataUser["contra_encript"]=contraEncript # reemplaza la contraOriginal por la encriptada
        # se pone la sintaxis de sql, consulta para insertar informacion en la tabla usuario
        query = text("""
            INSERT INTO usuario (
                nombre_completo, num_documento, correo,
                contra_encript, id_rol, estado
            ) VALUES (
                :nombre_completo, :num_documento, :correo,
                :contra_encript, :id_rol, :estado
            )
        """)
        # :nombre_completo, es un parametro de consulta que les llegan desde db.execute(query, dataUser)
        db.execute(query, dataUser) # execute ayuda a limpiar los datos y evitar una inyeccion sql
        db.commit()
        return True # retorna True cuando se ejecuta la insercion de datos correctamente en la tabla usuario
    except Exception as e: # e captura el tipo de error
        db.rollback() # Se regresa al momento anterior como un ctrl+z o deja las cosas como estaban
        logger.error(f"Error al crear usuario: {e}") # Guarda el error dentro del objeto logger
        raise Exception("Error de base de datos al crear el usuario") # raise propaga la respuesta y no termina la acción, esto va dirigida al endpoint. Exception no pude llevar el error capturado por e por seguridad informatica ya que traeria informacion sensible que puede ser utilizada por atacantes que pueden provocar los errores a proposito.
    

# funcion para consultar usuario por id
def get_user_by_id(db: Session, id_usuario:int):
    # el try except se usa para control de errores
    try:
        query = text ("""
            SELECT usuario.id_usuario, usuario.nombre_completo, 
            usuario.num_documento, usuario.correo, usuario.id_rol, 
            usuario.estado, rol.nombre_rol
            FROM usuario
            INNER JOIN rol ON usuario.id_rol = rol.id_rol
            WHERE usuario.id_usuario = :id_user
        """)
        
        result = db.execute(query, {"id_user": id_usuario}).mappings().first() # .mappings() convierte la tabla devuelta en un diccionario python; .first() sirve para seleccionar el primer resultado encontrado
        return result

    except SQLAlchemyError as e: # SQLAlchemyError permite capturar los errores que se generen en la interacción con la base de datos.
        logger.error(f"Error al consultar usuario: {e}")
        raise Exception("Error de base de datos al consultar un usuario")


# funcion para consultar usuario por correo
def get_user_by_email(db: Session, un_correo:str):
    # el try except se usa para control de errores
    try:
        query = text ("""
            SELECT usuario.id_usuario, usuario.nombre_completo,
                usuario.num_documento, usuario.correo, usuario.id_rol,
                usuario.estado, rol.nombre_rol
            FROM usuario
            INNER JOIN rol ON usuario.id_rol = rol.id_rol
            WHERE usuario.correo = :email
        """)
        # :email es un parametro de consulta, esta esperando un dato para la consulta que se asigna en email:un_correo
        result = db.execute(query, {"email": un_correo}).mappings().first() # .mappings() convierte la tabla devuelta en un diccionario python; .first() sirve para seleccionar el primer resultado encontrado
        return result

    except SQLAlchemyError as e:
        logger.error(f"Error al consultar usuario por correo: {e}")
        raise Exception("Error de base de datos al consultar un usuario por correo")

# funcion para consultar usuario por correo para seguridad
def get_user_by_email_security(db: Session, un_correo:str):
    # el try except se usa para control de errores
    try:
        query = text ("""
            SELECT usuario.id_usuario, usuario.nombre_completo, usuario.contra_encript, usuario.num_documento, usuario.correo, usuario.id_rol, usuario.estado, rol.nombre_rol
            FROM usuario
            INNER JOIN rol ON usuario.id_rol = rol.id_rol
            WHERE usuario.correo = :email
        """)
        # :email es un parametro de consulta, esta esperando un dato para la consulta que se asigna en email:un_correo
        result = db.execute(query, {"email": un_correo}).mappings().first() # .mappings() convierte la tabla devuelta en un diccionario python; .first() sirve para seleccionar el primer resultado encontrado
        return result

    except SQLAlchemyError as e:
        logger.error(f"Error al consultar usuario por correo: {e}")
        raise Exception("Error de base de datos al consultar un usuario por correo")

#Actualizar usuario por id
def update_user(db: Session, user_id: int, user_update: EditarUsuario) -> bool:
    try:
        fields = user_update.model_dump(exclude_unset=True)# el schema se convierte en json o diccionario y exclude_unset=True indica que se excluye todo lo que no llegue, es decir si llegan campos vacios se excluyen y se guarda en fields
        if not fields: # esto es por si no se envia campos para editar
            return False
        set_clause = ", ".join([f"{key} = :{key}" for key in fields]) # .join permite concatenar agregando datos, es mas potente, es separado por ", ", que permite construir una lista donde se recorre el diccionario fields y se extrae la key de cada pareja en el diccionario
        fields["user_id"] = user_id # se extrae el id del usuario para ser utilizado en la query

        query = text(f"UPDATE usuario SET {set_clause} WHERE id_usuario = :user_id")
        db.execute(query, fields)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar usuario: {e}") # se guarda en el archivo logger para tener una lista de errores y poder revisarlos
        raise Exception("Error de base de datos al actualizar el usuario")

# funcion para eliminar usuario por id
def user_delete(db: Session, id:int):
    # el try except se usa para control de errores
    try:
        query = text ("""
            DELETE FROM usuario
            WHERE usuario.id_usuario = :el_id
        """)
        # :el_id es un parametro de consulta, esta esperando un dato para la consulta que se asigna en "el_id": id
        db.execute(query, {"el_id": id})
        db.commit()
        return True

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al eliminar usuario por id: {e}")
        raise Exception("Error de base de datos al eliminar el usuario")

#Actualizar contraseña por id
# def update_password(db: Session, user_data: EditarPass) -> bool:
#     try:
#         datos_usuario = user_data.model_dump()
#         contra_encript = get_hashed_password(datos_usuario['contra_nueva'])
#         datos_usuario['pass_encript'] = contra_encript
        
#         query = text(f"""UPDATE usuario SET contra_encript = :pass_encript WHERE id_usuario = :id_usuario""")
#         db.execute(query, datos_usuario)
#         db.commit()
#         return True
#     except SQLAlchemyError as e:
#         db.rollback()
#         logger.error(f"Error al actualizar contraseña: {e}") # se guarda en el archivo logger para tener una lista de errores y poder revisarlos
#         raise Exception("Error de base de datos al actualizar contraseña")
    
def update_password(db: Session, user_data: EditarPass) -> bool:
    try:
        datos_usuario = user_data.model_dump()
        contra_encript = get_hashed_password(datos_usuario['contra_nueva'])
        datos_usuario['pass_encript'] = contra_encript # crea un nuevo par llave y valor guardando la clave encirptada nueva

        query = text(f""" UPDATE usuario SET contra_encript = :pass_encript 
                        WHERE id_usuario = :id_usuario """)
        
        db.execute(query, datos_usuario)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar usuario: {e}")
        raise Exception("Error de base de datos al actualizar el usuario")


def verify_user_pass(db: Session, user_data: EditarPass) -> bool:
    try:
        query = text("""
            SELECT usuario.contra_encript
            FROM usuario
            WHERE usuario.id_usuario = :id_user
        """)

        result = db.execute(query, {"id_user": user_data.id_usuario }).mappings().first()
        contra_en_db = result.contra_encript
        contra_anterior = user_data.contra_anterior
        print(contra_en_db)
        print(contra_anterior)

        validated = verify_password(contra_anterior, contra_en_db)

        if not validated:
            return False
        else:
            return True
    
    except SQLAlchemyError as e:
        logger.error(f"Error al buscar validar la contraseña: {e}")
        raise Exception("Error de base de datos al validar la contraseña")



def get_all_user(db: Session):
    try:
        query = text("""
            SELECT usuario.id_usuario, usuario.nombre_completo, 
                   usuario.num_documento, usuario.correo, usuario.id_rol, 
                   usuario.estado, rol.nombre_rol
            FROM usuario
            INNER JOIN rol ON usuario.id_rol = rol.id_rol
        """)

        result = db.execute(query).mappings().all()
        return result
    
    except SQLAlchemyError as e:
        logger.error(f"Error al bucar usuario: {e}")
        raise Exception("Error de base de datos al buscar el usuario")